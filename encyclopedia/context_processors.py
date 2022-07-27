from . import views

def add_variable_to_context(request):
    return ({
        "form": views.NewForm()
    })