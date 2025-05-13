from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import Annotated

app = FastAPI()

# ✅ Example 1: Simple Dependency Function
# Yeh function sirf ek static goal return karta hai
def get_simple_goal():
    return {"goal": "We are building AI Agents Workforce"}

@app.get("/get-simple-goal")
def simple_goal(
    response: Annotated[dict, Depends(get_simple_goal)]  # Depends use karke function ka result le rahe hain
):
    return response


# ✅ Example 2: Dependency with Parameter (Query se input le raha hai)
def get_goal(username: str):  # FastAPI automatically username ko query param banata hai
    return {
        "goal": "We are building AI Agents Workforce",
        "username": username
    }

@app.get("/get-goal")
def get_my_goal(
    response: Annotated[dict, Depends(get_goal)]
):
    return response


# ✅ Example 3: Dependency with Query Parameters and login logic
def dep_login(username: str = Query(None), password: str = Query(None)):
    # Hardcoded login check
    if username == "admin" and password == "admin":
        return {"message": "Login Successful"}
    return {"message": "Login Failed"}

@app.get("/signin")
def login_api(
    user: Annotated[dict, Depends(dep_login)]
):
    return user


# ✅ Example 4: Multiple Dependencies
# Dono functions num value ko increment kar rahe hain

def depfunc1(num: int):  # +1 kar raha hai
    return num + 1

def depfunc2(num: int):  # +2 kar raha hai
    return num + 2

@app.get("/main/{num}")
def get_main(
    num: int,
    num1: Annotated[int, Depends(depfunc1)],  # num + 1
    num2: Annotated[int, Depends(depfunc2)]   # num + 2
):
    total = num + num1 + num2
    return f"Pakistan {total}"  # 3 times num with additions


# ✅ Example 5: Class-based Dependency (like Database lookup)
# Dictionary ko fake database ki tarah use kar rahe hain
blogs = {
    "1": "Generative AI Blog",
    "2": "Machine Learning Blog"
}

# Yeh class kisi model (dict) mein id se object dhoondhti hai
# Agar nahi mila to 404 error raise karti hai
class GetObjectOr404():
    def __init__(self, model):
        self.model = model

    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(
                status_code=404,
                detail=f"Object {id} not found"
            )
        return obj

# Class ka instance 
blog_dependency = GetObjectOr404(blogs)

@app.get("/blog/{id}")
def get_blog(
    blog_name: Annotated[str, Depends(blog_dependency)]
):
    return blog_name
