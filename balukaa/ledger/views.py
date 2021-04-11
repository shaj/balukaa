from django.shortcuts import render

# Create your views here.
def main(request):
    # tasks = Task.objects.order_by('-id')
    return render(request, 'ledger/index.html',
                  {
                      'title': 'Главная страница сайта',
                      'tasks': 'test'
                  })
