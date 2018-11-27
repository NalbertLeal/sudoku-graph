def list_to_str(the_list):
  try:
    str_result = ''
    for element in the_list:
      str_result += str(element)
    return str_result
  except Exception as e:
    print(the_list)
    return the_list