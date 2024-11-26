import json
import sys

def calculator_tool(tool_input):
    """Performs a calculation based on the tool input."""
    try:
        num1 = float(tool_input['num1'])
        num2 = float(tool_input['num2'])
        operation = tool_input.get('operation', '+')

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                return {'error': "Division by zero"}
            result = num1 / num2
        else:
            return {'error': "Unsupported operation"}

        return {'result': result}
    except (KeyError, ValueError, TypeError) as e:
        return {'error': f"Invalid input: {e}"}

def claude_api_call(user_query):
    """
    This is a placeholder.  Replace this with your actual Claude API call.
    This example assumes the API returns a JSON string with 'tool' and 'parameters' keys.
    """
    # Example - replace with your actual API call
    if "calculate" in user_query.lower():
        try:
            num1, op, num2 = user_query.lower().replace("calculate ", "").split()
            return json.dumps({"tool": "calculator", "parameters": {"num1": num1, "num2": num2, "operation": op}})
        except ValueError:
            return json.dumps({"error": "Invalid query format. Use 'calculate num1 op num2'"})
    else:
        return json.dumps({"error": "No tool identified"})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ac.py <user_query>")
        sys.exit(1)

    user_query = sys.argv[1]
    claude_response = json.loads(claude_api_call(user_query))

    if "error" in claude_response:
        print(json.dumps({"error": claude_response["error"]}))
    elif claude_response["tool"] == "calculator":
        result = calculator_tool(claude_response["parameters"])
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Unsupported tool"}))

