from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.db.models import Q, F
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Contact
from .forms import ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        days_ahead = self.request.GET.get("days_ahead", None)
        user = self.request.user

        contacts = Contact.objects.filter(user=user)
        if query:
            contacts = contacts.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone__icontains=query)
                | Q(address__icontains=query)
            )

        if days_ahead:
            try:
                days_ahead = int(days_ahead)
                current_date = datetime.now().date()
                target_date = current_date + timedelta(days=days_ahead)

                current_month = current_date.month
                current_day = current_date.day
                target_month = target_date.month
                target_day = target_date.day

                if days_ahead == 0:
                    contacts = contacts.filter(
                        birthday__month=current_month,
                        birthday__day=current_day
                    )
                else:
                    # Check if the date range spans a year boundary
                    if current_date.year == target_date.year:
                        # Same year logic
                        same_year_query = (
                            Q(birthday__month__gt=current_month) |
                            Q(birthday__month=current_month, birthday__day__gte=current_day)
                        ) & (
                            Q(birthday__month__lt=target_month) |
                            Q(birthday__month=target_month, birthday__day__lte=target_day)
                        )
                        contacts = contacts.filter(same_year_query)

                    else:
                        # Cross-year logic (e.g., Dec 30 -> Jan 4)
                        cross_year_query = (
                            Q(birthday__month=current_month, birthday__day__gte=current_day) |
                            Q(birthday__month__gt=current_month)
                        ) | (
                            Q(birthday__month__lt=target_month) |
                            Q(birthday__month=target_month, birthday__day__lte=target_day)
                        )
                        contacts = contacts.filter(cross_year_query)

                
            except ValueError:
                pass

        return contacts.order_by(
            F("first_name").asc(nulls_last=True),
            F("last_name").asc(nulls_last=True),
        )


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")
