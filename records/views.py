from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicalRecord
from .forms import MedicalRecordForm


def record_list(request):

    records = MedicalRecord.objects.select_related('patient').all()

    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


def record_create(request):

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)

        if form.is_valid():
            record = form.save()
            return redirect('record_detail', pk=record.pk)

    else:
        form = MedicalRecordForm()

    return render(
        request,
        'records/record_form.html',
        {
            'form': form,
            'title': 'Nuevo expediente'
        }
    )


def record_detail(request, pk):

    record = get_object_or_404(
        MedicalRecord,
        pk=pk
    )

    return render(
        request,
        'records/record_detail.html',
        {'record': record}
    )


def record_update(request, pk):

    record = get_object_or_404(
        MedicalRecord,
        pk=pk
    )

    if request.method == 'POST':

        form = MedicalRecordForm(
            request.POST,
            instance=record
        )

        if form.is_valid():
            form.save()

            return redirect(
                'record_detail',
                pk=record.pk
            )

    else:
        form = MedicalRecordForm(
            instance=record
        )

    return render(
        request,
        'records/record_form.html',
        {
            'form': form,
            'title': 'Editar expediente'
        }
    )