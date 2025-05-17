def reverse_order_words(input_string):
    """
    This function takes a string as input and returns a new string with the words in reverse order.
    
    :param input_string: str, the input string to be reversed
    :return: str, the input string with words in reverse order
    """
    # Split the input string into words
    words = input_string.split()
    words= words[::-1]  # Reverse the list of words
    reversed_string = ' '.join(words)  # Join the reversed list of words into a single string
    return reversed_string

print("Reverse of the sentence is : ",reverse_order_words("Hello World"))  # Output: "World Hello"
print("Reverse of the sentence is : ",reverse_order_words("I love programming"))  # Output: "programming love I"
print("Reverse of the sentence is : ",reverse_order_words("Airflow is awesome"))  # Output: "awesome is Airflow"    