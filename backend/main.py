from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import io
import time
import traceback
import ast
from typing import Dict, List, Any, Optional
import json
import os
<<<<<<< HEAD

app = FastAPI(title="Code Visualizer API", version="1.0.0")

=======
from pymongo import MongoClient
import bcrypt

app = FastAPI(title="Code Visualizer API", version="1.0.0")

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["code_visualizer"]
users_collection = db["users"]

>>>>>>> 4e063f6 (login database)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    timeout: Optional[int] = 30  # Timeout in seconds

<<<<<<< HEAD
=======
class UserRequest(BaseModel):
    email: str
    password: str

>>>>>>> 4e063f6 (login database)
class CodeAnalysis(BaseModel):
    line_count: int
    function_count: int
    class_count: int
    import_count: int
    complexity_score: float
    syntax_valid: bool
    error_details: Optional[str] = None

def safe_serialize(val):
    """Enhanced serialization with better type handling and filtering"""
    if isinstance(val, (int, float, str, bool)) or val is None:
        return val
    elif isinstance(val, list):
        return [safe_serialize(v) for v in val]
    elif isinstance(val, dict):
        return {str(k): safe_serialize(v) for k, v in val.items()}
    elif isinstance(val, tuple):
        return tuple(safe_serialize(v) for v in val)
    elif isinstance(val, set):
        return list(safe_serialize(v) for v in val)
    elif hasattr(val, '__dict__'):
        # Handle custom objects
        return {
            '__class__': val.__class__.__name__,
            '__dict__': safe_serialize(val.__dict__)
        }
    else:
        return str(val)

def should_include_variable(name, value):
    """Filter out variables that shouldn't be displayed"""
    # Skip built-in functions and complex objects
    if name.startswith('__'):
        return False
    
    # Skip built-in functions
    if callable(value) and hasattr(value, '__module__') and value.__module__ == 'builtins':
        return False
    
    # Skip complex built-in objects
    if isinstance(value, (type, type(type))):
        return False
    
    # Skip very large objects that would clutter the display
    if isinstance(value, dict) and len(str(value)) > 500:
        return False
    
    return True

def analyze_code(code: str) -> CodeAnalysis:
    """Analyze code structure and complexity"""
    try:
        tree = ast.parse(code)
        
        line_count = len(code.split('\n'))
        function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        import_count = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
        
        # Simple complexity score based on control structures
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity += 1
        
        return CodeAnalysis(
            line_count=line_count,
            function_count=function_count,
            class_count=class_count,
            import_count=import_count,
            complexity_score=complexity,
            syntax_valid=True
        )
    except SyntaxError as e:
        return CodeAnalysis(
            line_count=len(code.split('\n')),
            function_count=0,
            class_count=0,
            import_count=0,
            complexity_score=0,
            syntax_valid=False,
            error_details=f"Syntax error at line {e.lineno}: {e.msg}"
        )
    except Exception as e:
        return CodeAnalysis(
            line_count=len(code.split('\n')),
            function_count=0,
            class_count=0,
            import_count=0,
            complexity_score=0,
            syntax_valid=False,
            error_details=str(e)
        )

# Add a global to hold code lines for tracing
code_lines_for_trace = []

# Global variable to store steps during tracing
tracing_steps = []

def trace_lines(frame, event, arg):
    global tracing_steps
    
    if event == 'line':
        lineno = frame.f_lineno
        filename = frame.f_code.co_filename
        
        # Filter variables to show only relevant ones
        local_vars = {}
        for k, v in frame.f_locals.items():
            if should_include_variable(k, v):
                local_vars[k] = safe_serialize(v)
        
        global_vars = {}
        for k, v in frame.f_globals.items():
            if should_include_variable(k, v):
                global_vars[k] = safe_serialize(v)
        
        # --- Split into arrays and scalars ---
        arrays = {}
        scalars = {}
        for k, v in local_vars.items():
            if isinstance(v, (list, tuple)):
                arrays[k] = v
            elif isinstance(v, (int, float, str, bool)) or v is None:
                scalars[k] = v

        # --- Track changed variables ---
        changed = []
        if tracing_steps:
            prev_step = tracing_steps[-1]
            prev_vars = prev_step.get('local_vars', {})
            for k, v in local_vars.items():
                if k not in prev_vars or prev_vars[k] != v:
                    changed.append(k)
        else:
            changed = list(local_vars.keys())

        # Add code line to step_info - fix index access
        try:
            code_line = code_lines_for_trace[lineno-1] if 0 < lineno <= len(code_lines_for_trace) else ""
        except (IndexError, NameError):
            code_line = ""

        step_info = {
            "line": lineno,
            "event": event,
            "local_vars": local_vars,  # Keep for change tracking
            "globals": global_vars,
            "arrays": arrays,
            "scalars": scalars,
            "function": frame.f_code.co_name,
            "filename": filename,
            "code": code_line,
            "changed": changed
        }
        
        tracing_steps.append(step_info)
    
    return trace_lines

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Code Visualizer Backend is running",
        "version": "1.0.0",
        "endpoints": {
            "/execute": "Execute and trace Python code",
            "/analyze": "Analyze code structure",
<<<<<<< HEAD
            "/health": "Health check"
        }
    }

=======
            "/health": "Health check",
            "/signup": "Sign up new user",
            "/login": "Login user"
        }
    }

# Signup endpoint
@app.post("/signup")
def signup(user: UserRequest):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({"email": user.email, "password": hashed.decode('latin1')})
    return {"message": "Signup successful"}

# Login endpoint
@app.post("/login")
def login(user: UserRequest):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found. Please sign up.")
    stored_hash = db_user["password"].encode('latin1')
    if not bcrypt.checkpw(user.password.encode(), stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

>>>>>>> 4e063f6 (login database)
@app.get("/health")
def health_check():
    """Detailed health check"""
    print("Health check requested")
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "python_version": sys.version,
        "platform": sys.platform
    }

@app.post("/analyze")
def analyze_code_endpoint(request: CodeRequest):
    """Analyze code structure without executing it"""
    analysis = analyze_code(request.code)
    return {
        "analysis": analysis.dict(),
        "status": "success"
    }

@app.post("/execute")
def execute_code(request: CodeRequest):
    """Execute code with enhanced tracing and error handling"""
    print(f"Received execute request with code: {request.code[:100]}...")
    code = request.code
    timeout = request.timeout or 30
    global code_lines_for_trace
    code_lines_for_trace = code.splitlines()
    
    # Reset tracing state
    global tracing_steps
    tracing_steps = []
    
    # Analyze code first
    analysis = analyze_code(code)
    
    if not analysis.syntax_valid:
        return {
            "steps": [],
            "output": "",
            "status": "syntax_error",
            "error": analysis.error_details,
            "analysis": analysis.dict()
        }
    
    start_time = time.time()
    
    try:
        # Create a safe execution environment
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'type': type,
                'isinstance': isinstance,
                'sum': sum,
                'max': max,
                'min': min,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'reversed': reversed,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'any': any,
                'all': all,
                'chr': chr,
                'ord': ord,
                'hex': hex,
                'bin': bin,
                'oct': oct,
                'format': format,
                'repr': repr,
                'ascii': ascii,
                'divmod': divmod,
                'pow': pow,
                'hash': hash,
                'id': id,
                'callable': callable,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'delattr': delattr,
                'dir': dir,
                'vars': vars,
                'globals': globals,
                'locals': locals,
                'eval': eval,
                'exec': exec,
                'compile': compile,
                'open': open,
                'input': input,
                'help': help,
                'quit': quit,
                'exit': exit,
                'copyright': copyright,
                'credits': credits,
                'license': license,
                'True': True,
                'False': False,
                'None': None,
                'Ellipsis': Ellipsis,
                'NotImplemented': NotImplemented,
                'Exception': Exception,
                'BaseException': BaseException,
                'TypeError': TypeError,
                'ValueError': ValueError,
                'IndexError': IndexError,
                'KeyError': KeyError,
                'AttributeError': AttributeError,
                'NameError': NameError,
                'SyntaxError': SyntaxError,
                'IndentationError': IndentationError,
                'ZeroDivisionError': ZeroDivisionError,
                'OverflowError': OverflowError,
                'MemoryError': MemoryError,
                'OSError': OSError,
                'FileNotFoundError': FileNotFoundError,
                'PermissionError': PermissionError,
                'TimeoutError': TimeoutError,
                'ConnectionError': ConnectionError,
                'BrokenPipeError': BrokenPipeError,
                'ConnectionRefusedError': ConnectionRefusedError,
                'ConnectionResetError': ConnectionResetError,
                'ConnectionAbortedError': ConnectionAbortedError,
                'BlockingIOError': BlockingIOError,
                'InterruptedError': InterruptedError,
                'IsADirectoryError': IsADirectoryError,
                'NotADirectoryError': NotADirectoryError,
                'FileExistsError': FileExistsError,
                'ProcessLookupError': ProcessLookupError,
                'ChildProcessError': ChildProcessError,
                'RecursionError': RecursionError,
                'UnboundLocalError': UnboundLocalError,
                'UnicodeError': UnicodeError,
                'UnicodeDecodeError': UnicodeDecodeError,
                'UnicodeEncodeError': UnicodeEncodeError,
                'UnicodeTranslateError': UnicodeTranslateError,
                'LookupError': LookupError,
                'ArithmeticError': ArithmeticError,
                'FloatingPointError': FloatingPointError,
                'AssertionError': AssertionError,
                'BufferError': BufferError,
                'EOFError': EOFError,
                'ImportError': ImportError,
                'ModuleNotFoundError': ModuleNotFoundError,
                'RuntimeError': RuntimeError,
                'NotImplementedError': NotImplementedError,
                'ReferenceError': ReferenceError,
                'SystemError': SystemError,
                'TabError': TabError,
                'Warning': Warning,
                'UserWarning': UserWarning,
                'DeprecationWarning': DeprecationWarning,
                'PendingDeprecationWarning': PendingDeprecationWarning,
                'SyntaxWarning': SyntaxWarning,
                'RuntimeWarning': RuntimeWarning,
                'FutureWarning': FutureWarning,
                'ImportWarning': ImportWarning,
                'UnicodeWarning': UnicodeWarning,
                'BytesWarning': BytesWarning,
                'ResourceWarning': ResourceWarning,
                'GeneratorExit': GeneratorExit,
                'KeyboardInterrupt': KeyboardInterrupt,
                'SystemExit': SystemExit,
                'StopIteration': StopIteration,
                'StopAsyncIteration': StopAsyncIteration,
                'BaseExceptionGroup': BaseExceptionGroup,
                'ExceptionGroup': ExceptionGroup,
            }
        }
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        
        # Set up tracing
        sys.settrace(trace_lines)
        
        # Execute with timeout protection
        exec(code, safe_globals)
        
        # Clean up tracing
        sys.settrace(None)
        output = mystdout.getvalue()
        sys.stdout = old_stdout
        
        execution_time = time.time() - start_time
        
        result = {
            "steps": tracing_steps,
            "output": output,
            "status": "success",
            "execution_time": execution_time,
            "analysis": analysis.dict(),
            "memory_usage": len(tracing_steps)  # Simple metric
        }
        print(f"Execution successful, returning {len(tracing_steps)} steps")
        return result
        
    except Exception as e:
        # Clean up on error
        sys.settrace(None)
        if 'mystdout' in locals():
            sys.stdout = old_stdout
        
        execution_time = time.time() - start_time
        
        # Enhanced error information
        error_info = {
            "type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        
        result = {
            "steps": tracing_steps,
            "output": "",
            "status": "error",
            "error": error_info,
            "execution_time": execution_time,
            "analysis": analysis.dict()
        }
        print(f"Execution failed: {error_info['type']}: {error_info['message']}")
        return result

@app.get("/examples")
def get_examples():
    """Get example code snippets"""
    return {
        "examples": {
            "hello_world": {
                "name": "Hello World",
                "code": 'print("Hello, World!")',
                "description": "Simple print statement"
            },
            "variables": {
                "name": "Variables and Types",
                "code": '''x = 10
y = "Hello"
z = [1, 2, 3]
print(f"x: {x}, y: {y}, z: {z}")''',
                "description": "Working with different variable types"
            },
            "loop": {
                "name": "For Loop",
                "code": '''for i in range(5):
    print(f"Number: {i}")''',
                "description": "Simple for loop"
            },
            "function": {
                "name": "Function Definition",
                "code": '''def greet(name):
    return f"Hello, {name}!"

result = greet("Alice")
print(result)''',
                "description": "Defining and calling a function"
            },
            "list_comprehension": {
                "name": "List Comprehension",
                "code": '''numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print(f"Original: {numbers}")
print(f"Squares: {squares}")''',
                "description": "List comprehension example"
            }
        }
    }

class AIExplainRequest(BaseModel):
    code: str
    step_info: str
    current_step: int
    total_steps: int

@app.post("/ai_explain")
async def ai_explain(request: AIExplainRequest):
    """Generate simple AI explanation for a code step"""
    try:
        # Simple built-in explanation system
        explanation = generate_simple_explanation(request.code, request.step_info, request.current_step, request.total_steps)
        return {"explanation": explanation}
        
    except Exception as e:
        print(f"AI explanation error: {e}")
        return {"explanation": "AI explanation is currently unavailable."}

def generate_simple_explanation(code: str, step_info: str, current_step: int, total_steps: int) -> str:
    """Generate simple explanations based on code patterns"""
    code_lower = code.lower().strip()
    step_info_lower = step_info.lower()
    
    # Parse step info to understand what's happening
    if "for" in code_lower and "range" in code_lower:
        if "i" in code_lower and "j" in code_lower:
            return "This is a nested loop structure. The outer loop (i) controls the main iteration, while the inner loop (j) handles comparisons within each pass. This is typical in sorting algorithms like bubble sort."
        else:
            return "This is a loop iteration. We're going through each element in the collection to perform some operation."
    
    elif "if" in code_lower:
        return "This is a conditional check. We're evaluating whether a certain condition is true, and if so, we'll execute the code inside this block."
    
    elif "=" in code_lower and not "==" in code_lower:
        # Assignment operation
        if "swap" in step_info_lower or "exchange" in step_info_lower:
            return "This is a swap operation. We're exchanging the values of two variables to reorder elements in the array."
        else:
            return "This is an assignment operation. We're storing a value in a variable for later use."
    
    elif "print" in code_lower or "console.log" in code_lower:
        return "This is an output statement. We're displaying information to help us understand what's happening during execution."
    
    elif "def" in code_lower or "function" in code_lower:
        return "This is a function definition. We're creating a reusable block of code that can be called multiple times."
    
    elif "return" in code_lower:
        return "This is a return statement. We're sending a value back from this function to wherever it was called from."
    
    elif "len" in code_lower or "length" in step_info_lower:
        return "We're getting the length or size of a data structure to understand how many elements we're working with."
    
    elif "arr" in code_lower or "array" in step_info_lower:
        if "sort" in step_info_lower:
            return "We're working with array elements in a sorting algorithm. This step is part of the process of organizing the array in a specific order."
        else:
            return "We're accessing or modifying elements in an array. Arrays store multiple values that we can access by their position."
    
    elif "temp" in code_lower or "temporary" in step_info_lower:
        return "We're using a temporary variable to store a value temporarily. This is often used in swap operations or when we need to preserve a value."
    
    elif current_step == 0:
        return "This is the initialization step. We're setting up the variables and data structures we'll need for the algorithm to work properly."
    
    elif current_step == total_steps - 1:
        return "This is the final step. The algorithm has completed its work and we're seeing the final result or cleanup operations."
    
    else:
        # Generic explanation based on step position
        progress = (current_step / total_steps) * 100
        if progress < 25:
            return "We're in the early stages of the algorithm. This step is part of the setup and initial processing phase."
        elif progress < 50:
            return "We're in the middle of the algorithm execution. This step is part of the main processing logic."
        elif progress < 75:
            return "We're approaching the end of the algorithm. This step is part of the final processing phase."
        else:
            return "We're in the final stages of the algorithm. This step is preparing for completion or performing final operations."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)