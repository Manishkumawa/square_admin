from django.shortcuts import render,redirect ,HttpResponse 
from django.http import JsonResponse
from django.core.paginator import Paginator
import mysql.connector
from django.views.decorators.csrf import csrf_exempt
import requests
from django.conf import settings
# Create your views here.
from .models import UserData
from django.core.serializers import serialize
from django.contrib.auth import authenticate, login, logout
from .models import *
from demo_app.data_temp import *
from .extractPdf import extract
import datetime
from django.conf import settings

def index(request):
    
    if request.method =='POST':

        username   = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = UserData.objects.filter(email = email)
        if user:
            return redirect('/login')

        if password != confirm_password:
            return render(request,'error.html',{'error':'Password not match'})
        
        else:
            user = UserData(username = username ,email = email,password = password,confirm_password =confirm_password)
            user.save()
            return redirect('login')
        
    return render(request,'signup.html')

def total_item(request):

    user_data = select_data()
    return render(request ,'temp.html' ,{'user_data':user_data})

def login(request):

    if request.method =='POST':

        username = request.POST['username']
        password = request.POST['password']

        print(username)
        print(password)

        
        check_user = UserData.objects.filter(username = username ,password =password)

        if check_user:

            request.session['user'] = username
            return redirect('total_item')
        
        
    return render(request,'login.html')
def logout(request):

    try:
        del request.session['user']

    except:
        return redirect('login')
    
    return redirect('login')


def data(request):
    myconn = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
    cursor = myconn.cursor()


    cursor.execute("SELECT COUNT(*) FROM square_insurance.pdf_text_extract")
    total_records = cursor.fetchone()[0]

    print(total_records)

    # Calculate pagination offset and fetch data for the requested page

    cursor.execute("SELECT COUNT(*) FROM square_insurance.pdf_text_extract")
    total_records = cursor.fetchone()[0]

    print(total_records)

    # Pagination parameters
    per_page = 10  # Number of records per page
    page_number = int(request.GET.get('page', 1))
    offset = (page_number - 1) * per_page

    # Search query
    search_query = request.GET.get('search[value]', None)
    query_params = ('%' + search_query + '%',) if search_query else ()

    # Fetch data based on pagination and search criteria
    query = "SELECT * FROM square_insurance.pdf_text_extract"
    if search_query:
        query += " WHERE insurer LIKE %s"  # Adjust this based on your search criteria
    query += " LIMIT %s OFFSET %s"
    cursor.execute(query, query_params + (per_page, offset))
    data = cursor.fetchall()

    # Format fetched data into a list of dictionaries
    data_list = []
    for row in data:
        data_list.append({
            'id': row[0],
            'insurer': row[1],
            'datas': row[2],
            'created_at': row[3],
            'updated_at': row[4]
        })

    # Close cursor and connection
    cursor.close()
    myconn.close()

    # Return JSON response with data, total records, and filtered records
    return JsonResponse({'data': data_list, 'recordsTotal': total_records, 'recordsFiltered': total_records})

def server_side(request):
    return render(request, 'server.html')

def server2(request):


    
    return render(request ,'server2.html')


def data_detail(request,id):


    myconn = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
    cursor = myconn.cursor()

    sql  ="select *from square_insurance.pdf_text_extract where id =%s "
    val = (id ,)
    cursor.execute(sql,val)

    data = cursor.fetchone()

    if data:
        data_dict = {
            'id': data[0],
            'insurer': data[1],
            'datas': data[2],
            'created_at': data[3],
            'updated_at': data[4]
        }
    
    else:
        data_dict = {}

    cursor.close()
    myconn.close()

    return JsonResponse(data_dict)


def handle_uploaded_file(f):
    upload_folder = os.path.join(settings.MEDIA_ROOT, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file_path = os.path.join(upload_folder, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def upload_data(request):
    
    if request.method =='POST':

        insurer = request.POST.get('insurer')
        lob = request.POST.get('lob')
        product = request.POST.get('product')
        product_plan_type = request.POST.get('productPlanType')
        file_upload = request.FILES.get('fileUpload')

        if file_upload:
            file_path = handle_uploaded_file(file_upload)
            datas = extract(file_path)

            datas = json.dumps(datas)

        
        myconn = mysql.connector.connect(host=os.getenv("HOST"), user=os.getenv("USER"), passwd=os.getenv("PASSWORD"), database=os.getenv("DATABASE"))
        cursor = myconn.cursor()
        
        sql  ="Insert into square_insurance.pdf_text_extract (insurer,datas ,created_at ,lob ,product ,product_plan_type) values(%s,%s,%s,%s,%s,%s)"
        created_at = datetime.datetime.now()
        values =(insurer,datas,created_at,lob,product,product_plan_type)

        cursor.execute(sql,values)

        myconn.commit()


        
        
        
        return render(request ,'successful.html')
            
    return render(request ,'pdf_for_extract.html')
        




    
       
        
            
    

def masters(request) :
    return render(request,'all_finance.html') 

@csrf_exempt
def update_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Data received:", data)
            file_path = r'https://www.squareinsurance.in/testing/new_motor/uploads/financer/all.json'

            # Load the JSON data from the file
            with open(file_path, 'r') as file:
                records = json.load(file)
            
            # Find and update the record
            record_found = False
            for record in records:
                
                if str(record['id']) == str(data['id']):  # Ensure both are strings for comparison
                    record['financier_id'] = data['financier_id']
                    record['financier_name'] = data['financier_name']
                    record['status'] = data['status']
                    record_found = True

                    print("Updated record:", record)
                    break

            if not record_found:
                return JsonResponse({'success': False, 'error': 'Record not found'})

            # Write the updated records back to the file
            with open(file_path, 'w') as file:
                json.dump(records, file, separators=(',', ':'))

            return JsonResponse({'success': True})
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
def add_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Data received:", data)

            file_path = r'C:\Users\Manish Kumawat\OneDrive\Desktop\Admin_demo\Admin_demo\media\uploads\all_financier.json'

            # Load the JSON data from the file
            with open(file_path, 'r') as file:
                records = json.load(file)
            
            

            length = len(records)
            temp = {
                'id':length+1,
                'financier_id' : data['financier_id'],
                'financier_name':data['financier_name'],
                'status' :data['status'],
            }
            records.append(temp)
            
            # Write the updated records back to the file
            with open(file_path, 'w') as file:
                json.dump(records, file, separators=(',', ':'))

            return redirect('masters')
        except Exception as e:
            print("Error:", str(e))
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})





def data_masters(request):
    file_path = os.path.join(settings.UPLOADS_DIR, 'all_financier.json')
    print(file_path)

    with open(file_path,'r') as pdf:
        data = json.load(pdf)
        length = int(request.GET.get('length', 10))
        paginator = Paginator(data, length)  # Show `length` records per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Extract search value from request
        search_value = request.GET.get('search[value]', '')

        # Filter data based on search value if search value is provided
        if search_value:
            filtered_data = []
            for item in data:
                if search_value.lower() in str(item['financier_id']).lower() or search_value.lower() in str(item['financier_name']).lower():
                    filtered_data.append(item)
        else:
            filtered_data = data

        # Paginate filtered data
        paginator_filtered = Paginator(filtered_data, length)
        page_obj_filtered = paginator_filtered.get_page(page_number)

        data_list = []
        for item in page_obj_filtered.object_list:
            temp = {
                'id': item['id'],
                'financier_id': item['financier_id'],
                'financier_name': item['financier_name'],
                'status': item.get('status', 'Inactive')  # Default to 'Inactive' if 'status' is not present
            }
            data_list.append(temp)

        draw = int(request.GET.get('draw', 1))

        return JsonResponse({
            'data': data_list,
            'recordsTotal': len(data),
            'recordsFiltered': len(filtered_data),
            'draw': draw,
            'totalRows': len(data_list)
        })
    
    

