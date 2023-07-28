class Angle:
    def __init__(self, p_pos, c1_pos, c2_pos, p_d, c1_d, c2_d, branch_level):
        self.parent_position = p_pos
        self.children1_position = c1_pos
        self.children2_position = c2_pos
        self.parent_direction = p_d
        self.children1_direction = c1_d
        self.children2_direction = c2_d
        self.branch_level = branch_level






