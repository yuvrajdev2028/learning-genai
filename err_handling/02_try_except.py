menu = ['matar paneer', 'chicken rara', 'chicken biryani']

def take_order(item):
    try:
        if(item not in menu):
            raise ValueError(f"Sorry! We do not serve {item}.")
        else:
            print(f"Order taken for {item}")
    except ValueError as e:
        print("Error: ",e)
    finally:
        print("Next order please.")

take_order('Kofta')
take_order('chicken biryani')