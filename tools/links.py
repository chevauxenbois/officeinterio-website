"""Which catalogue items appear (as similar pieces) in which projects.
Used by build_projects.py and build_products.py to link the two both ways."""

PROJECTS = {
    'alfa': dict(name='Alfa', cover='images/projects/alfa/workstations-sm.jpg'),
    'gamma': dict(name='Gamma', cover='images/projects/gamma/booths-sm.jpg'),
    'marathon-futurex': dict(name='Marathon Futurex', cover='images/projects/marathon-futurex/open-workspace-sm.jpg'),
}

USED = {
    'alfa': ['workstation-with-screens', 'linear-workstation', 'task-chair', 'pantry-set'],
    'gamma': ['linear-workstation', 'task-chair', 'boardroom-table', 'meeting-table', 'reception-desk', 'lounge-set'],
    'marathon-futurex': ['linear-workstation', 'task-chair', 'reception-desk', 'manager-desk', 'meeting-table', 'lounge-set'],
}


def projects_using(product_slug):
    return [p for p, items in USED.items() if product_slug in items]
