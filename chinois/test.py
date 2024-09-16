from rich.console import Console
from rich.text import Text

def check_mistakes(str1, str2):
    console = Console()
    output = Text()

    # Compare each character of both strings
    for i, char in enumerate(str1):
        if i < len(str2):
            if char == str2[i]:
                output.append(char, style="bold green")  # Correct character
            else:
                output.append(char, style="bold red")    # Incorrect character
        else:
            output.append(char, style="bold red")        # Extra character in str1

    # If str2 is longer than str1, highlight the extra characters in str2
    if len(str2) > len(str1):
        output.append(f" (Missing: {str2[len(str1):]})", style="bold yellow")

    # Print the result
    console.print(output)
    return output



def main():
    user_ans = "wo3 shi4 fa3 guo4 ren2"
    correct_ans = "wo3 shi4 fa3 guo2 ren2"
    check_mistakes(user_ans, correct_ans)

if __name__ == "__main__":
    main()