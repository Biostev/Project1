# Chemical dictionary
Can tell you everything about the chemical according to the entered `chemical formula`, and if it doesn't know, you can add it to the `database`!

# Features
- You can enter your formula and see info about this element or chemical. If the formula is not in db, you can add it
- Molecular mass for chemicals is calculated automatically
- Сonvenient info showing as a table. It is editable, so you can update info about chemical or element easyly
- You can delete element or chemical from the database by clicking delete button
- Easy to use

# Dependencies
- PyQt5

Characteristics:
- Chemical elements:
- - Formula
- - Name
- - Section
- - Period
- - Atomic number
- - Atomic mass
- - Density
- - Melting point
- - Boiling point
- Chemicals:
- - Formula
- - Molecular mass
- - Name
- - Density
- - Melting point
- - Boiling point
- - Thermal conductivity
- - Electrical conductivity

# Interface
There is an input field in the MainWindow. Enter your chemical formula there. Then the InfoWindow will appear.
InfoWindow has a table and 2 buttons: Update data and Delete. You can change info in the table, but some rows are read-only (Formula for both and checical also has a read-only molecular mass). After changing you can click Update data button and the database will be updated with it. Also you can delete element/chemical from the database by clicking Delete button.

# Interface screenshots
![MainWindow](https://github.com/Biostev/Project1/blob/main/Interface/MainWindow.png)
![InfoWindowForChemicals](https://github.com/Biostev/Project1/blob/main/Interface/InfoWindowForChemicals.png)
![InfoWindowForElements](https://github.com/Biostev/Project1/blob/main/Interface/InfoWindowForElements.png)
![UnknownFormula](https://github.com/Biostev/Project1/blob/main/Interface/UnknownFormula.png)
![IncorrectInput](https://github.com/Biostev/Project1/blob/main/Interface/IncorrectInput.png)

# Authors
- [Biostev](https://github.com/Biostev)
