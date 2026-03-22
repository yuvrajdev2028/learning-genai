# Index Error -> IndexError: list index out of range
# games = ['cricket','football']

# print(games[2])

# ---------------------------------------------------------------------------------------

# Key Error -> KeyError: 'England'
# player_country_map = {
#     "Australia":['Michael Clarke', 'Steve Smith', 'Brett Lee', 'Shane Warne', 'Shane Watson'],
#     "India":['Sachin Tendulkar', 'Virat Kohli', 'MS Dhoni', 'Shikhar Dhawan', 'Rohit Sharma', 'Jasprit Bumrah', 'Kapil Dev']
# }

# print(player_country_map['India']) # Works Fine
# print(player_country_map['England']) # Throws key error

# ---------------------------------------------------------------------------------------

# Zero Division Error -> ZeroDivisionError: division by zero
# num1 = 10
# num2 = 0
# res = num1 / num2
# print(res)

# ---------------------------------------------------------------------------------------

# Type Error

# print('2' + 2) # TypeError: can only concatenate str (not "int") to str

# a = 10
# a() # TypeError: 'int' object is not callable

# teams = ['Chennai', 'Mumbai', 'Kolkata']
# print(teams['1']) # TypeError: list indices must be integers or slices, not str

# ---------------------------------------------------------------------------------------

# Name Error -> NameError: name 'non_existing_variable' is not defined

# print(non_existing_variable)

# ---------------------------------------------------------------------------------------

# Value Error

# int("abc") # ValueError: invalid literal for int() with base 10: 'abc'