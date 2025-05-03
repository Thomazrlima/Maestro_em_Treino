def my_obj_reader(filename: str) -> list:
    """Get the vertices from the OBJ file (considering v/vt/vn format)."""
    position_list = list()
    vertices = list()

    with open(filename, 'r') as in_file:
        for line in in_file:
            if line.startswith('v '):
                point = [float(value) for value in line.strip().split()[1:]]
                vertices.append(point)
            elif line.startswith('f'):
                face_description = line.strip().split()[1:]
                for value in face_description:
                    vertex_index = int(value.split('/')[0]) - 1
                    position_list.append(vertices[vertex_index])

    return position_list
