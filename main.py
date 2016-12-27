from nbt_parser import nbt as parser

class structure(parser.NBTFile):
    def __init__(self,path=None):

        if path is not None:
            parser.NBTFile.__init__(self,path,"rb")
        else:
            parser.NBTFile.__init__(self,"MCStructure/template.nbt","rb")
            self.set_size()
            self["blocks"]=parser.TAG_List(type=parser.TAG_Compound)
            self["entities"]=parser.TAG_List(type=parser.TAG_Compound)
            self["palette"]=parser.TAG_List(type=parser.TAG_Compound)

    def set_size(self,x=1,y=1,z=1):
        self["size"].tags[0].value=x
        self["size"].tags[1].value=y
        self["size"].tags[2].value=z

    def add_block_to_palette(self,block_id,properties=None):
        self["palette"].append(parser.TAG_Compound())
        self["palette"].tags[-1].tags.append(parser.TAG_String(name="Name",value=block_id))

        if properties is not None:
            properties_tag=parser.TAG_Compound()
            properties_tag.name="Properties"
            for k,v in properties.items():
                properties_tag.tags.append(parser.TAG_String(name=k,value=v))
            self["palette"].tags[-1].tags.append(properties_tag)

    def place_block(self,state,x,y,z,nbt=None):
        self["blocks"].append(parser.TAG_Compound())

        block_pos = parser.TAG_List(name="pos", type=parser.TAG_Int)
        block_pos.tags.extend([parser.TAG_Int(x),parser.TAG_Int(y),parser.TAG_Int(z)])
        self["blocks"].tags[-1].tags.append(block_pos)
        self["blocks"].tags[-1].tags.append(parser.TAG_Int(name="state",value=state))

        if nbt is not None:
            block_nbt=parser.TAG_Compound()
            block_nbt.name="nbt"
            for k,v in nbt.items():
                if type(v) is str:
                    block_nbt.tags.append(parser.TAG_String(name=k,value=v))
                if type(v) is long:
                    block_nbt.tags.append(parser.TAG_Long(name=k,value=v))
                if type(v) is bool:
                    block_nbt.tags.append(parser.TAG_Byte(name=k,value=v))
            self["blocks"].tags[-1].tags.append(block_nbt)

    def fill_area(self,state,x,y,z,dx,dy,dz,nbt=None):
        for ix in range(x,dx):
            for iy in range(y,dy):
                for iz in range(z,dz):
                    self.place_block(state,ix,iy,iz,nbt)

    def replace_blocks(self,state_1,state_2,nbt_1=None,nbt_2=None):
        for b in self["blocks"].tags:
            if int(str(b["state"])) == state_1:
                if nbt_1 is not None and b["nbt"]==nbt_1:
                    b["state"]=parser.TAG_Int(state_2)
                    b["nbt"]=parser.TAG_Int(nbt_2)
                if nbt_1 is None:
                    b["state"]=parser.TAG_Int(state_2)

    def place_entity(self,is_precise,x,y,z,nbt):
        self["entities"].append(parser.TAG_Compound())

        entity_pos_precise = parser.TAG_List(name="pos", type=parser.TAG_Double)
        if is_precise:
            entity_pos_precise.tags.extend([parser.TAG_Double(x),parser.TAG_Double(y),parser.TAG_Double(z)])
        else:
            entity_pos_precise.tags.extend([parser.TAG_Double(x+.5),parser.TAG_Double(y),parser.TAG_Double(z+.5)])

        entity_pos = parser.TAG_List(name="blockPos", type=parser.TAG_Int)
        entity_pos.tags.extend([parser.TAG_Int(x),parser.TAG_Int(y),parser.TAG_Int(z)])
        self["entities"].tags[-1].tags.extend([entity_pos,entity_pos_precise])

        entity_nbt=parser.TAG_Compound()
        entity_nbt.name="nbt"
        for k,v in nbt.items():
            if type(v) is str:
                entity_nbt.tags.append(parser.TAG_String(name=k,value=v))
            if type(v) is long:
                entity_nbt.tags.append(parser.TAG_Long(name=k,value=v))
            if type(v) is bool:
                entity_nbt.tags.append(parser.TAG_Byte(name=k,value=v))
        self["entities"].tags[-1].tags.append(entity_nbt)

    def get_block_state(self,block_id,properties=None):
        for p in self["palette"].tags:
            if str(p["Name"])==block_id:
                for k,v in properties.iteritems():
                    if str(p["Properties"][k])!=v:
                        return False
                return self["palette"].tags.index(p)

    def is_coordinate_in_structure(self,x,y,z):
        if (int(str(self["size"].tags[0])) <= x) or (x<0):
            return False
        elif (int(str(self["size"].tags[1])) <= y) or (y<0):
            return False
        elif (int(str(self["size"].tags[2])) <= z) or (z<0):
            return False
        else:
            return True

    def find_and_replace_nbt(self,find_substring,replace_substring,key):
        for b in self["blocks"]:
            try:
                b["nbt"][key]=parser.TAG_String(str(b["nbt"][key]).replace(find_substring,replace_substring))
            except:
                pass


    def save(self,path="structure"):
        self.write_file(path)
