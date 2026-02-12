from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import SessionNote
from consultants.models import ConsultantSession

@login_required
def view_session_notes(request, session_id):
    session = get_object_or_404(
        ConsultantSession,
        id=session_id,
        user=request.user
    )

    note = SessionNote.objects.filter(session=session).first()

    return render(request, "session_notes/view.html", {
        "session": session,
        "note": note
    })
