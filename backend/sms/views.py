import csv
from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Purchase, IssuedItem, Items, Faculty, Department
from django.db.models import Sum
from django.db import transaction
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


@staff_member_required
def index(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item = Items.objects.filter(
            name=item_name,
            is_active=True
        ).first()

        if item is None:
            messages.error(
                request,
                'This item is inactive or does not exist.'
            )
            return redirect('index')
        quantity = request.POST.get('quantity')
        rate = request.POST.get('rate')
        invoice_number = request.POST.get('invoice_number')
        billing_date = request.POST.get('billing_date')
        date_of_entry = request.POST.get('date_of_entry')
        total_amount = request.POST.get('total_amount')
        seller_name = request.POST.get('seller_name')
        cgst = request.POST.get('cgst')
        sgst = request.POST.get('sgst')
        extra_charges = request.POST.get('extra_charges')

        Purchase.objects.create(
            ItemName=item,
            Quantity=quantity,
            Rate=rate,
            Invoice_Number=invoice_number,
            Billing_Date=billing_date,
            Date_of_Entry=date_of_entry,
            Total_Amount=total_amount,
            Seller_Name=seller_name,
            CGST=cgst,
            SGST=sgst,
            Extra_charges=extra_charges
        )

        messages.success(request, 'Data submitted!')
        return redirect('index')

    submitted = False
    purchases = Purchase.objects.all()
    message_list = messages.get_messages(request)

    return render(request, 'Purchase.html', {
        'purchases': purchases,
        'submitted': submitted,
        'messages': message_list,
        'item_names': Items.objects.filter(
            is_active=True
        ).values_list('name', flat=True)
    })


@staff_member_required
def issued(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        try:
            quantity = int(request.POST.get('quantity', ''))
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, 'Enter a valid quantity greater than zero.')
            return redirect('issued')
        employee_name = request.POST.get('employee_name')
        issue_date_str = request.POST.get('issue_date')
        department_name = request.POST.get('department')
        refrence_No = request.POST.get('refrence_No')
        location = request.POST.get('location')

        try:
            # Get the item from the Items table
            item = Items.objects.filter(
                name=item_name,
                is_active=True
            ).first()

            if item is None:
                messages.error(
                    request,
                    'This item is inactive or does not exist.'
                )
                return redirect('issued')

            # Check if there are enough items in inventory
            if item.QuantityInInventory < quantity:
                messages.error(request, 'Not enough items in inventory.')
                return redirect('issued')

            # Get the employee from the Faculty table
            employee = Faculty.objects.filter(
                name=employee_name,
                is_active=True
            ).first()

            if employee is None:
                messages.error(
                    request,
                        'This faculty member is inactive or does not exist.'
                )
                return redirect('issued')

            # Get the department from the Department table
            department = get_object_or_404(Department, department=department_name)

            # Convert issue_date string to a datetime object
            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()

            # Use a transaction to ensure atomicity
            with transaction.atomic():
                # Create and save IssuedItem
                issued_item = IssuedItem.objects.create(
                    ItemName=item,
                    Quantity=quantity,
                    Name_of_Employee=employee,
                    Issue_Date=issue_date,
                    Department=department,
                    Refrence_No=refrence_No,
                    Location=location,
                )

                # Update the quantity in the Items model
                item.QuantityInInventory -= quantity
                item.ItemsIssued += quantity
                item.save()

            # Add a success message
            messages.success(request, 'Item issued!')
            return redirect('issued')

        except Items.DoesNotExist:
            return HttpResponse("Item not found in Items table")

        except Faculty.DoesNotExist:
            return HttpResponse("Employee not found in Faculty table")

        except Department.DoesNotExist:
            return HttpResponse("Department not found in Department table")

    # Fetch data to be displayed in the template
    issued_items = IssuedItem.objects.all()
    faculty_names = Faculty.objects.filter(is_active=True)
    items = Items.objects.filter(
        is_active=True
    ).values_list('name', flat=True).distinct()
    departments = Department.objects.all()
    message_list = messages.get_messages(request)

    return render(request, 'Issued.html', {'faculty_names': faculty_names, 'items': items, 'issued_items': issued_items, 'departments': departments, 'messages': message_list})
 



@staff_member_required
def dashboard(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')

        # Convert item name to lowercase for consistency
        item_name_upper = item_name.upper()

        # Check if an item with the same name (case-insensitive) already exists
        existing_item = Items.objects.filter(name__iexact=item_name_upper).first()

        try:
            item = Items.objects.get(name=existing_item)
            messages.error(request, 'Item already exists.')

        except ObjectDoesNotExist:
            Items.objects.create(
                name=item_name_upper,
                totalPurchased=0,
                ItemsIssued=0,
                QuantityInInventory=0
            )
            messages.success(request, 'New item added successfully.')

    # Fetch all unique item names from the Purchase table
    items = Purchase.objects.values_list('ItemName__name', flat=True).distinct()

    # Create a list to store information for each item
    item_info_list = []

    # Calculate total purchased and total issued quantities for each item
    for item_name in items:
        total_purchased = Purchase.objects.filter(ItemName__name=item_name).aggregate(Sum('Quantity'))['Quantity__sum'] or 0
        total_issued = IssuedItem.objects.filter(ItemName__name=item_name).aggregate(Sum('Quantity'))['Quantity__sum'] or 0

        # Calculate items in inventory for each item
        inventory = total_purchased - total_issued

        # Save or update the data in the Items model
        item, created = Items.objects.get_or_create(name=item_name)
        item.totalPurchased = total_purchased
        item.ItemsIssued = total_issued
        item.QuantityInInventory = inventory
        item.save()

        # Append item information to the list
        item_info_list.append({
            'name': item_name,
            'total_purchased': total_purchased,
            'total_issued': total_issued,
            'inventory': inventory,
        })

    return render(request, 'dashboard.html', {'item_info_list': item_info_list})
@staff_member_required
def export_purchases_csv(request):
    """Export purchase history as a UTF-8 CSV file."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="purchase-history.csv"'
    response.write('\ufeff')  # Helps spreadsheet applications detect UTF-8.
    writer = csv.writer(response)
    writer.writerow([
        'Item Name', 'Quantity', 'Rate', 'Invoice Number', 'Billing Date',
        'Date of Entry', 'Total Amount', 'Seller Name', 'CGST', 'SGST',
        'Extra Charges', 'GST'
    ])
    for purchase in Purchase.objects.select_related('ItemName').order_by('id'):
        writer.writerow([
            purchase.ItemName.name, purchase.Quantity, purchase.Rate,
            purchase.Invoice_Number, purchase.Billing_Date,
            purchase.Date_of_Entry, purchase.Total_Amount,
            purchase.Seller_Name, purchase.CGST, purchase.SGST,
            purchase.Extra_charges, purchase.GST
        ])
    return response


@staff_member_required
def export_issued_csv(request):
    """Export issued-item history as a UTF-8 CSV file."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="issue-history.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'Item Name', 'Quantity', 'Employee Name', 'Issue Date',
        'Department', 'Reference Number', 'Location', 'Physical Verification'
    ])
    for issued_item in IssuedItem.objects.select_related(
        'ItemName', 'Name_of_Employee', 'Department'
    ).order_by('id'):
        writer.writerow([
            issued_item.ItemName.name, issued_item.Quantity,
            issued_item.Name_of_Employee.name, issued_item.Issue_Date,
            issued_item.Department.department, issued_item.Refrence_No,
            issued_item.Location, issued_item.physical_verification
        ])
    return response


def reports(request):
    return render(request, 'reports.html')

def home(request):
    return render(request, 'landing.html')


def profile(request):
    return render(request,'Profile.html')