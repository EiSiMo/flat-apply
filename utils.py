def str_to_preview(string, max_length):
    if not max_length > 3:
        raise ValueError('max_length must be greater than 3')

    first_line = string.split('\n')[0]
    if len(first_line) > max_length:
        return first_line[:max_length-3] + '...'
    return first_line