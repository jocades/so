from rich.prompt import Prompt, Confirm, IntPrompt
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.padding import Padding
from rich.progress import Progress
from rich.tree import Tree
from time import sleep

c = Console()


x = Prompt.ask("What is your name?", password=True)
c.log(type(x))

y = Confirm.ask("Do you like this library?", default=True)
c.print(type(y))

z = IntPrompt.ask("How many do you want?")
c.print(type(z))

with c.status("Working..."):
    sleep(2)
    c.log("Done!")

style = 'bold white on blue'

c.print('Hello world!', style=style, justify='left')
# how to add padding to the right so as it justified
c.print('Hello world!', style=style, justify='right')


print(Panel('Hello world!', title='Panel', ))


def p(content, x=4, y=0):
    return Padding(content, (y, x))


print(p('Padding', y=1))


tree = Tree('root')
tree.add('child1')
tree.add('child2')

subtree = tree.add('child3')
subtree.add('grandchild1')

print(tree)


# Link
print('Here is https://jocades.dev')
