import re
from pathlib import Path


cwd = Path.cwd()
src = cwd / 'src'

actions = {
    'list': 'list',
    'post': 'create',
    'get': 'get',
    'put': 'update',
    'delete': 'delete'
}

templates = {
    'routes': {
        'list': lambda name: f"router.get('/', {name})\n",
        'post': lambda name: f"router.post('/', {name})\n",
        'get': lambda name: f"router.get('/:id', {name})\n",
        'put': lambda name: f"router.put('/:id', {name})\n",
        'delete': lambda name: f"router.delete('/:id', {name})\n",
    },
    'handlers': {
        'list': lambda model: f"router.get('/', handler.list({model}))\n",
        'post': lambda model: f"router.post('/', validate({model.lower()}Body), handler.createOne({model}))\n",
        'get': lambda model: f"router.get('/:id', validateId, handler.getOne({model}))\n",
        'put': lambda model: f"router.put('/:id', [validateId, validate({model.lower()}Body)], handler.updateOne({model}))\n",
        'delete': lambda model: f"router.delete('/:id', [validateId, validate({model.lower()}Body)], handler.deleteOne({model}))\n",
    },
    'models': {
        'import': lambda model: f"import {model.capitalize()} from '../models/{model.lower()}.model'",
    },
}


class Writer:
    def __init__(
            self,
            name: str,
            with_model: bool = False,
            with_handler: bool = False
    ):
        name = name.lower()
        self.name = name
        self.with_model = with_model
        self.with_handler = with_handler

        self.controller_path = src / 'routes' / f"{name}s" / f"{name}s.controller.ts"
        self.route_path = src / 'routes' / f"{name}s" / f"{name}s.route.ts"
        self.routes_index = src / 'routes' / 'index.ts'
        self.model_path = src / 'models' / f"{name}.model.ts"
        self.app_path = src / 'start' / 'app.ts'

    def write(self, methods: list[str] | None):
        if not self.controller_path.parent.exists():
            self.controller_path.parent.mkdir()

        if not self.route_path.parent.exists():
            self.route_path.parent.mkdir()

        if not methods:
            methods = 'list post get put delete'.split()
        else:
            methods = [method.lower() for method in methods]
            methods.sort(key=lambda method: 'list post get put delete'.index(method))

        if self.with_handler:
            self.route_path.write_text(self.route_with_handler_template(methods))
        else:
            self.controller_path.write_text(self.controller_template(methods))
            self.route_path.write_text(self.route_template(methods))

        if self.with_model:
            self.model_path.write_text(self.model_template())

        # self.append_to_index()
        # self.append_to_app()

    def controller_name(self, method: str):
        return f"{actions[method]}{self.name.capitalize()}{'s' if method == 'list' else ''}"

    def controller_template(self, methods: list[str]):
        template = "import { RequestHandler } from 'express'\n"
        if self.with_model:
            template += templates['models']['import'](self.name) + '\n'
        for method in methods:
            template += f"""
export const {self.controller_name(method)}: RequestHandler = (req, res) => {{
  res.send('{method.upper()} {self.name}')
}}
"""
        return template

    def route_template(self, methods: list[str]):
        template = f"""import {{ Router }} from 'express'
import {{ {', '.join(self.controller_name(method) for method in methods)} }} from './{self.name}s.controller'

const router = Router()\n
"""
        for method in methods:
            controller = self.controller_name(method)
            template += templates['routes'][method](controller)
        template += "\nexport default router\n"
        return template

    def route_with_handler_template(self, methods: list[str]):
        template = f"""import {{ Router }} from 'express'
import {{ validateId, validate }} from '../../middleware'
import {self.name.capitalize()}, {{ {self.name}Body }} from '../../models/{self.name}.model'
import handler from '../../lib/controller-factory'

const router = Router()\n
"""
        for method in methods:
            template += templates['handlers'][method](self.name.capitalize())
        template += "\nexport default router\n"
        return template

    def route_with_framework_template(self, methods: list[str]):
        template = f"""import {{ app }} from '../../framework/app'"""
        if self.with_model:
            template += f"""{templates['models']['import'](self.name)}\n
app.route(
  '/{self.name}s', {{
  model: {self.name.capitalize()},
}})
"""

    def model_template(self):
        model_name = self.name.capitalize()
        return f"""import {{ Schema, model, Types, Model }} from 'mongoose'
const {{ ObjectId }} = Types
import {{ z }} from 'zod'

export interface I{model_name} extends BaseModel {{
  name: string
}}

interface I{model_name}Methods {{}}

type {model_name}Doc = Model<I{model_name}, {{}}, I{model_name}Methods>

const {self.name}Schema = new Schema<I{model_name}, {model_name}Doc, I{model_name}Methods>(
  {{
    name: {{ type: String, required: true }},
  }},
  {{ timestamps: true }}
)

export default model<I{model_name}, {model_name}Doc>('{model_name}', {self.name}Schema)

export const {self.name}Body = z.object({{
  name: z.string().min(3).max(255)
}})
"""

    def append_to_index(self):
        content = self.routes_index.read_text()
        # content += f"export {{ default as {self.name}sRouter }} from './{self.name}s.route'\n"
        content += f"import ./routes/{self.name}s.route'\n"
        self.routes_index.write_text(content)

    def append_to_app(self):
        content = self.app_path.read_text()
        content = re.sub(r"import { (.*) } from '../routes'",
                         r"import { \1, " + self.name + r"sRouter } from '../routes'", content)
        content_lines = content.splitlines(keepends=True)

        i = 0
        for i, line in enumerate(content_lines):
            if line.startswith('app.use(error)'):
                break

        content_lines.insert(i - 1, f"app.use('/api/{self.name}s', {self.name}sRouter)\n")
        self.app_path.write_text(''.join(content_lines))
