from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datalake.models import Dataset


def home(request):
    return render(request, "index.html")


@login_required
def dashboard(request):

    # Sirf logged-in user ka data
    datasets = Dataset.objects.filter(user=request.user)

    total_files = datasets.count()

    valid_files = datasets.filter(
        status="Validated"
    ).count()

    invalid_files = datasets.filter(
        status="Invalid"
    ).count()

    recent_files = datasets.order_by("-uploaded_at")[:5]

    if total_files > 0:
        metadata = int((valid_files / total_files) * 100)
    else:
        metadata = 100

    context = {
        "total_files": total_files,
        "valid_files": valid_files,
        "invalid_files": invalid_files,
        "metadata": metadata,
        "recent_files": recent_files,
        "username": request.user.username,
    }

    return render(request, "dashboard.html", context)