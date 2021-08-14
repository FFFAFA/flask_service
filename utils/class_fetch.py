def get_class_name(class_id):
    # Read CUB-200-2011 classes file to get class name
    class_file = open('/home/zhaoxue/services/flask_service/classes.txt', 'r')
    class_name = ''
    for line in class_file.readlines():
        number_n_name = line.split(' ')
        number = number_n_name[0]
        original_class_name = number_n_name[1].split('.')[1]
        if number == str(class_id):
            name_words = original_class_name.split('_')
            class_name = name_words[0]
            for word in name_words[1:]:
                if word[0].islower():
                    word = '-' + word
                else:
                    word = ' ' + word
                class_name = class_name + word
            # Remove trailing new line
            class_name = class_name[0:len(class_name)-1]
            print("Class name fetched: " + class_name)
            break
    class_file.close()
    return class_name
