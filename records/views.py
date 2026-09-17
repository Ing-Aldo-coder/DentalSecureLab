from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import MedicalRecord
from .forms import MedicalRecordForm


@login_required
def record_list(request):
    # Validación estricta de control de acceso y rol
    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):
        raise PermissionDenied("Acceso denegado: Únicamente personal médico o administradores pueden acceder a los expedientes clínicos.")

    records = MedicalRecord.objects.select_related('patient').all()

    return render(
        request,
        'records/record_list.html',
        {'records': records}
    )


@login_required
def record_create(request):
    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):
        raise PermissionDenied("Acceso denegado: Únicamente personal médico o administradores pueden crear expedientes clínicos.")

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)

        if form.is_valid():
            record = form.save()
            return redirect('record_detail', uuid=record.uuid)

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


@login_required
def record_detail(request, uuid=None, pk=None):
    # Verificación de rol y protección contra BOLA / IDOR
    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):
        raise PermissionDenied("Acceso denegado: Consulta de expediente restringida por política de confidencialidad.")

    if uuid is not None:
        record = get_object_or_404(MedicalRecord, uuid=uuid)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    return render(
        request,
        'records/record_detail.html',
        {'record': record}
    )


@login_required
def record_update(request, uuid=None, pk=None):
    if not (hasattr(request.user, 'role') and request.user.role in ['admin', 'doctor']):
        raise PermissionDenied("Acceso denegado: Modificación de expediente restringida por política de confidencialidad.")

    if uuid is not None:
        record = get_object_or_404(MedicalRecord, uuid=uuid)
    else:
        record = get_object_or_404(MedicalRecord, pk=pk)

    if request.method == 'POST':
        form = MedicalRecordForm(
            request.POST,
            instance=record
        )

        if form.is_valid():
            form.save()

            return redirect(
                'record_detail',
                uuid=record.uuid
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