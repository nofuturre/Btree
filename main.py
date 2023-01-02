from Menu import Menu

if __name__ == '__main__':
    vm = input("To enable verbose mode press v, any other key to continue\n")
    menu = Menu((vm == 'v'), 2)

    menu.print_menu()