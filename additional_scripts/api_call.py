import re
import subprocess
import requests

API_SOCKET = "http://localhost:8000/api"

SYNC_ENDPOINT = "/sync_generate"

NUM_RUNS = 5

MODEL = "deepseek-coder-v2:16b"

VERILOG_CODE_EXTRACTION_PATTERN = r"```verilog(.*?)```"

ROLE = "You are a computer engineer specialized in RTL modeling with Verilog."

ORIGINAL_CODE_REQUIREMENTS = """finite-state machine of the master side of a component that has an output implementing a 
simple handshake protocol with the following details:
- The reset must be synchronous
- Add a start input signal as the start condition when equals to one
- Deassert the request signal in the same cycle the ack from the slave arrives
Additionally, implement the code for the corresponding slave module to the previously 
generated master module.
"""

ORIGINAL_TESTBENCH_REQUIREMENTS = """
Generate testbenches for this code including assert for the output variables and only output the code without any explanation
"""

ORIGINAL_CODE_ACTION = """Write the code for: """ + ORIGINAL_CODE_REQUIREMENTS

ORIGINAL_CODE_GENERATION_PROMPT = ROLE + ORIGINAL_CODE_ACTION + """
Avoid generating any explanations about the implementation, just generate the Verilog code.
"""

CODE_FILE_PATH = "code.sv"

TEST_FILE_PATH = "test.sv"

def generate_correction_prompt(code: str, error: str):
    code_fix_prompt = ROLE + """Your action is to modify the provided code to fix the indicated errors. Code description: """ + ORIGINAL_CODE_REQUIREMENTS + """
    Code:""" + code +"""
    Previous code contains the following errors in the indicated lines:
    """ + error +"""
    
    Detect and fix the indicated errors in the code taking into account the description and provide only the fixed code.
    """
    return code_fix_prompt

def code_generation(prompt: str):
    data = {'prompt': prompt,
            'model': MODEL}
    request = requests.post(url=API_SOCKET + SYNC_ENDPOINT, json=data)
    response = request.content.decode('utf-8')
    matches = re.findall(VERILOG_CODE_EXTRACTION_PATTERN, response, re.DOTALL)
    readable_code = matches[0].encode().decode('unicode_escape')
    return readable_code

def generate_testbench_prompt(code: str):
    testbench_generation_prompt = ROLE + """ Given the following code: """ +code+ """\n""" + ORIGINAL_TESTBENCH_REQUIREMENTS
    return testbench_generation_prompt

def write_verilog_code_file(content: str):
    f = open(CODE_FILE_PATH, "w")
    f.write(content)
    f.close()

def write_verilog_test_file(content: str):
    f = open(TEST_FILE_PATH, "w")
    f.write(content)
    f.close()

def evaluate_verilog_code():
    # Build the command
    command = ["iverilog", "-g2012", "-o", "sim.out", CODE_FILE_PATH]
    is_execution_correct = True
    output = "Done"
    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            check=True,  # Raises CalledProcessError if command fails
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Print the outputs
        #print("Standard Output:")
        #print(result.stdout)
        #print("\nStandard Error:")
        #print(result.stderr)

        if result.returncode == 0:
            is_execution_correct = True
            print("\nCompilation successful! Output file: sim.out")
        else:
            print("\nCompilation failed")

    except subprocess.CalledProcessError as e:
        is_execution_correct = False
        #print(f"Error executing command: {e}")
        #print(f"Command output: {e.stdout}")
        #print(f"Command error: {e.stderr}")
        output = e.stderr
    except FileNotFoundError:
        print("Error: iverilog command not found. Make sure it's installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        return is_execution_correct, output

is_execution_correct = False
prompt = ORIGINAL_CODE_GENERATION_PROMPT
while not is_execution_correct and NUM_RUNS > 0:
    print('#########################----- AVAILABLE RUNS:{} -----#########################'.format(NUM_RUNS))
    code = code_generation(prompt=prompt)
    if code:
        write_verilog_code_file(code)
        is_execution_correct, output = evaluate_verilog_code()
        output = output.replace("I give up.", "")
        if not is_execution_correct:
            print(output)
            prompt = generate_correction_prompt(code = code, error = output)
    NUM_RUNS -= 1

