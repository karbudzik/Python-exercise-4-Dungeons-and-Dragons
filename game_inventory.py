def display_inventory(inventory):
    """Display the contents of the inventory in a simple way."""
    for item in inventory:
        print(item + ':', inventory[item])


def add_to_inventory(inventory, added_items):
    """Add to the inventory dictionary a list of items from added_items."""
    for item in added_items:
        if item in inventory.keys():
            inventory.update({item: inventory[item] + 1})
        else:
            inventory.update({item: 1})
    return inventory


def remove_from_inventory(inventory, removed_items):
    """Remove from the inventory dictionary a list of items from removed_items."""
    for item in removed_items:
        if item in inventory.keys():
            inventory.update({item: inventory[item] - 1})
            if inventory[item] <= 0:
                del inventory[item]
    return inventory


def print_table(inventory, order='empty'):
    """
    Display the contents of the inventory in an ordered, well-organized table with
    each column right-aligned.
    """
    column_widths = calculate_column_widths(inventory)
    inventory = sort_dictionary(inventory, order)

    print_line(column_widths)
    print('item name'.rjust(column_widths[0]) + ' | ' + 'count'.rjust(column_widths[1]))
    print_line(column_widths)
    for item in inventory:
        print(item.rjust(column_widths[0]) + ' | ' + str(inventory[item]).rjust(column_widths[1]))
    print_line(column_widths)


# ----- Helper functions for print_table START-----
def calculate_column_widths(inventory):
    """ Calculates the perfect widths of columns for printing purposes. """
    inventory.update({'item name': 'count'})
    key_lengths = [len(key) for key in inventory.keys()]
    value_lengths = [len(str(value)) for value in inventory.values()]
    column_widths = [max(key_lengths), max(value_lengths)]
    del inventory['item name']
    return column_widths


def sort_dictionary(inventory, order):
    """ Sorts the dictionary in a given order. """
    if order == 'count,asc':
        inventory = {k: v for k, v in sorted(inventory.items(), key=lambda inv_item: inv_item[1])}
    elif order == 'count,desc':
        inventory = {k: v for k, v in sorted(inventory.items(), key=lambda inv_item: inv_item[1], reverse=True)}
    return inventory


def print_line(column_widths):
    """ Prints straight line which length corresponds to column widths. """
    print("-" * (sum(column_widths) + len(column_widths) + 1))
# ----- Helper functions for print_table END -----


def import_inventory(inventory, filename='import_inventory.csv'):
    """Import new inventory items from a CSV file."""
    try:
        with open(filename, 'r') as inventory_file:
            new_inventory_items = inventory_file.readline().split(',')
            return add_to_inventory(inventory, new_inventory_items)
    except FileNotFoundError:
        print(f"File '{filename}' not found!")


def export_inventory(inventory, filename='export_inventory.csv'):
    """Export the inventory into a CSV file."""
    try:
        with open(filename, 'w') as inventory_file:
            inventory_line = ''
            for item in inventory:
                inventory_line += (item + ',') * inventory[item]
            inventory_file.writelines(inventory_line[:-1])  # write the inventory_line to a file without last ','
    except IOError:
        print(f"You don't have permission creating file '{filename}'!")


def main():
    pass


if __name__ == "__main__":
    main()
