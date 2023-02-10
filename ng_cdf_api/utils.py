def get_models_choices(choices):
    """_summary_

    Args:
        choices (_type_): _description_
    """
    choices_value_list = []
    for i in range(len(choices)):
        choices_value_list.append(choices[i][0])
    return choices_value_list