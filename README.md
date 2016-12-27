# MC-Structure
Wrapper for structure blocks on the Python NBT Parser

Parser: https://github.com/twoolie/NBT

###Classes:
structure(path) - Creates a structure block object

###Functions:
set_size(x,y,z) - Sets the size of the structure (default is 1,1,1)

add_block_to_palette(name,properties) - Adds block to palette

place_block(state,x,y,z,nbt) - Places block

fill_area(state,x,y,z,dx,dy,dz,nbt) - Fills an area with a block

replace_block(state,state_2,nbt,nbt_2) - Replaces all state blocks with state_2 blocks

place_entity(is_precise,x,y,z,nbt) - Places an entity

get_block_state(name,properties) - Returns a blocks state in the palette

is_coordinate_in_structure(x,y,z) - Returns if coordinate exists in the structure

find_and_replace_nbt(find,replace,key) - Replaces all instances of string 'find' with string 'replace' if the key matches

save(path) - Saves a structure block object

###Key:
x,y,z - Integers representing size or coordinates

name - String representing the name of a block E.G 'minecraft:stone'

properties - Dictionary representing differnt properties of a block E.G {'color':'black'}

state - Integer representing a blocks position in the palette

nbt - Dictionary representing the nbt of a block or entity E.G {'CustomName':'Phil'}

dx,dy,dz - Integers representing size

is_precise - Boolean representhing whether the entity is centered on the coordinates

find,replace - Strings

key - String representing a nbt key E.G 'CustomName'

