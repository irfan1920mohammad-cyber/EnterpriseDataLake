from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required

from .forms import DatasetForm
from .models import Dataset

import pandas as pd
import os
import hashlib


@login_required
def upload_dataset(request):

    if request.method == "POST":

        form = DatasetForm(request.POST, request.FILES)

        if form.is_valid():

            dataset = form.save(commit=False)

            # Logged in user ko assign karo
            dataset.user = request.user

            dataset.save()

            extension = os.path.splitext(dataset.file.name)[1].lower()

            if extension == ".csv":
                dataset.file_type = "CSV"
            elif extension == ".xlsx":
                dataset.file_type = "Excel"
            elif extension == ".json":
                dataset.file_type = "JSON"
            elif extension == ".xml":
                dataset.file_type = "XML"
            elif extension in [".jpg", ".jpeg", ".png"]:
                dataset.file_type = "Image"
            elif extension == ".pdf":
                dataset.file_type = "PDF"
            elif extension == ".mp4":
                dataset.file_type = "Video"
            else:
                dataset.file_type = "Other"

            sha256 = hashlib.sha256()

            with open(dataset.file.path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)

            dataset.file_hash = sha256.hexdigest()
            dataset.file_size = dataset.file.size

            try:

                if extension == ".csv":

                    df = pd.read_csv(dataset.file.path)

                    total_columns = len(df.columns)

                    dataset.total_columns = total_columns
                    dataset.valid_columns = total_columns
                    dataset.invalid_columns = 0
                    dataset.status = "Validated"

                else:

                    dataset.status = "Uploaded"

            except Exception:

                dataset.status = "Invalid"

            dataset.save()

            return redirect("/upload/")

    else:

        form = DatasetForm()

    search = request.GET.get("search")

    # Sirf current user ki files
    datasets = Dataset.objects.filter(
        user=request.user
    ).order_by("-id")

    if search:
        datasets = datasets.filter(file__icontains=search)

    return render(
        request,
        "upload.html",
        {
            "form": form,
            "datasets": datasets,
        },
    )


@login_required
def delete_dataset(request, id):

    dataset = get_object_or_404(
        Dataset,
        id=id,
        user=request.user
    )

    if dataset.file:
        dataset.file.delete(save=False)

    dataset.delete()

    return redirect("/upload/")


@login_required
def download_dataset(request, id):

    dataset = get_object_or_404(
        Dataset,
        id=id,
        user=request.user
    )

    return FileResponse(
        open(dataset.file.path, "rb"),
        as_attachment=True
    )


@login_required
def file_details(request, id):

    dataset = get_object_or_404(
        Dataset,
        id=id,
        user=request.user
    )

    return render(
        request,
        "details.html",
        {
            "dataset": dataset
        }
    )