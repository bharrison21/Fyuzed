from django.shortcuts import render, get_object_or_404, redirect
from . models import Course, Listing
from . forms import CourseCreationForm, ListingCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView, DetailView

from django.utils.text import slugify

import requests
from bs4 import BeautifulSoup as soup
import textwrap

# Create your views here.
@login_required
def create_course(request):
    user = request.user
    context = {
            'form': CourseCreationForm,
        }
    if request.method == 'POST':
        _title = request.POST['_title']
        _listing = request.POST['_listing']
        _info = request.POST['_info']
        _desc = request.POST['_desc']
        _urls = request.POST['_urls']

        listing_obj = get_object_or_404(Listing, pk = _listing)
        course = Course.objects.create(title = _title, listing = listing_obj, info = _info, desc = _desc, urls = _urls)

    
    return render(request, 'courses/create_course.html', context)


@login_required
def create_listing(request):
    user = request.user
    context = {
            'form': ListingCreationForm,
        }
    if request.method == 'POST':
        _name = request.POST['_name']
        _info = request.POST['_info']

        listing = Listing.objects.create(name = _name, info = _info)

    
    return render(request, 'courses/create_listing.html', context)




class Listings(LoginRequiredMixin, ListView):
    model = Listing
    template_name = "courses/listings.html"



class ViewListing(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'courses/view_listing.html'
    #handles slug from urls (slug is url path that differs between models, 
    #   so different groups have different urls)
    slug_url_kwarg = 'the_slug'
    slug_field = 'slug'


    def get_context_data(self, **kwargs):
        # self.request.session.set['cur_group'] = Group.objects.get_object_or_404(Group, slug = slug_field)
        context = super().get_context_data(**kwargs)
        return context



def fill_listing(request):
    r = requests.get('https://webapps.lsa.umich.edu/CrsMaint/Public/CB_PublicBulletin.aspx?crselevel=ug/robots.txt')

    page  = soup(r.text, "html.parser")
    subjects = []
    subject_tags = page.find('select', {'name':'ctl00$ContentPlaceHolder1$ddlSubject'}).findAll('option')
    for tag in subject_tags:
        if "Select" not in str(tag):
            subjects.append(tag.text)
            
    def wrapper(text: str, width: int = 120) -> str:
        return "\n".join(textwrap.wrap(text, width=width)) + "\n"

    _listing = Listing(name="Course Listing", info="current course listing")
    _listing.save()

    for subject in subjects:

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://webapps.lsa.umich.edu',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://webapps.lsa.umich.edu/CrsMaint/Public/CB_PublicBulletin.aspx?crselevel=ug/robots.txt',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        params = (
            ('crselevel', 'ug/robots.txt'),
        )

        data = {
        'ctl00$ContentPlaceHolder1$ddlTerm': '2310',
        'ctl00$ContentPlaceHolder1$ddlAttr': '',
        'ctl00$ContentPlaceHolder1$ddlPage': '9999',
        'ctl00$ContentPlaceHolder1$ddlSubject': subject,
        'ctl00$ContentPlaceHolder1$ddlDept': '',
        'ctl00$ContentPlaceHolder1$chbShowDescr': 'on',
        'ctl00$ContentPlaceHolder1$chbShowCGTerms': 'on',
        'ctl00$ContentPlaceHolder1$btnSearch': 'Search',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwUKMTEyOTU5NTYzMw8WBB4IaW50UGdJZHgCAR4Mc3RyQ3JzZUxldmVsBQJ1ZxYCZg9kFgICAw9kFgICAw9kFggCAw8WAh4EVGV4dAUcVW5kZXJncmFkdWF0ZSBDb3Vyc2UgQ2F0YWxvZ2QCBQ9kFgJmD2QWCAIBDxAPFgYeDkRhdGFWYWx1ZUZpZWxkBQR0ZXJtHg1EYXRhVGV4dEZpZWxkBQp0ZXJtX2Rlc2NyHgtfIURhdGFCb3VuZGdkEBUHCUZhbGwgMjAyMAtTdW1tZXIgMjAyMBJTcHJpbmcvU3VtbWVyIDIwMjALU3ByaW5nIDIwMjALV2ludGVyIDIwMjAJRmFsbCAyMDE5C1N1bW1lciAyMDE5FQcEMjMxMAQyMzAwBDIyOTAEMjI4MAQyMjcwBDIyNjAEMjI1MBQrAwdnZ2dnZ2dnFgFmZAIDDxAPFgYfAwUFdmFsdWUfBAUEdGV4dB8FZ2QQFQ8QU2VsZWN0IGFuIG9wdGlvbhNCYWNoZWxvciBvZiBTY2llbmNlGENyZWF0aXZlIEV4cHJlc3Npb24gKENFKQ9IdW1hbml0aWVzIChIVSkWSW50ZXJkaXNjaXBsaW5hcnkgKElEKR5NYXRoICYgU3ltYm9saWMgQW5hbHlzaXMgKE1TQSkVTmF0dXJhbCBTY2llbmNlcyAoTlMpFFNvY2lhbCBTY2llbmNlcyAoU1MpGUZpcnN0IFllYXIgV3JpdGluZyAoRllXUikITGFuZ3VhZ2UfUXVhbnRpdGF0aXZlIFJlYXNvbmluZyAxIChRUi8xKR9RdWFudGl0YXRpdmUgUmVhc29uaW5nIDIgKFFSLzIpFlJhY2UgJiBFdGhuaWNpdHkgKFImRSkMRXhwZXJpZW50aWFsEUluZGVwZW5kZW50IFN0dWR5FQ8AAkJTB0Rpc3QtQ0UHRGlzdC1IVQdEaXN0LUlECERpc3QtTVNBB0Rpc3QtTlMHRGlzdC1TUwJJQwhMYW5nX1JlcQRRUi8xBFFSLzICUkUERVhQUgRJTkRTFCsDD2dnZ2dnZ2dnZ2dnZ2dnZxYBZmQCBw8QDxYGHwMFB1N1YmplY3QfBAUHU3ViamVjdB8FZ2QQFaUBEFNlbGVjdCBhbiBvcHRpb24DQUFTBEFFUk8DQUxBBkFNQ1VMVAdBTkFUT01ZCEFOVEhSQVJDCEFOVEhSQklPCEFOVEhSQ1VMB0FQUFBIWVMGQVJBQkFNBkFSQUJJQwRBUkNICEFSTUVOSUFOCEFSVFNBRE1OBUFTSUFOCEFTSUFOTEFOCEFTSUFOUEFNBUFTVFJPAkJBA0JDUwJCRQZCSU9JTkYIQklPTENIRU0HQklPTE9HWQdCSU9NRURFB0JJT1BIWVMHQklPU1RBVAdDQVRBTEFOA0NFRQNDSEUEQ0hFTQNDSUMDQ0pTBkNMQVJDSAVDTENJVgdDTElNQVRFBkNMTElORwhDTVBMWFNZUwZDT0dTQ0kEQ09NTQRDT01QB0NPTVBMSVQDQ1NQBUNaRUNIBURBTkNFB0RBVEFTQ0kHRElHSVRBTAVEVVRDSAVFQVJUSANFQVMERUNPTghFRENVUklOUwdFRFNQQ0hSBEVEVUMDRUVCBEVFQ1MDRUhTA0VMSQdFTkdMSVNIBEVOR1IDRU5TBkVOU0NFTgdFTlZJUk9OBkZSRU5DSARGVFZNBEdFT0cGR0VSTUFOBUdSRUVLCEdSRUVLTU9EB0dUQk9PS1MGSEJFSEVEBkhFQlJFVwdISVNUQVJUB0hJU1RPUlkGSE9OT1JTAkhTBkhVTUdFTgdJTlNUSFVNB0lOVExTVEQGSU5UTUVEA0lPRQVJU0xBTQdJVEFMSUFOCEpBUEFORVNFBEpBWloGSlVEQUlDBUtSU1REBExBQ1MFTEFUSU4ITEFUSU5PQU0ETElORwhNQUNST01PTARNQVRIB01BVFNDSUUETUNEQgdNRUNIRU5HBk1FTEFORwRNRU1TBU1FTkFTA01GRwhNSUNSQklPTAdNSURFQVNUBk1JTFNDSQdNVVNFVU1TB01VU0lDT0wHTVVTTUVUSAhNVVNUSFRSRQhOQVRJVkVBTQZOQVZTQ0kETkVSUwhORVVST1NDSQROVVJTCE9SR1NUVURZA1BBVAdQRVJTSUFOBFBISUwHUEhZU0lDUwdQSFlTSU9MBlBPTElTSAZQT0xTQ0kGUE9SVFVHA1BQRQVQU1lDSAZQVUJQT0wEUU1TUwZSQ0FSVFMFUkNBU0wGUkNDT1JFBlJDSFVNUwZSQ0lESVYGUkNMQU5HBlJDTlNDSQZSQ1NTQ0kFUkVFRVMIUkVMSUdJT04HUk9NTEFORwdST01MSU5HB1JVU1NJQU4DU0FTBVNDQU5EBFNFQVMCU0kGU0xBVklDAlNNA1NPQwVTUEFDRQdTUEFOSVNIBFNTRUEFU1RBVFMHU1REQUJSRAhTVVJWTUVUSAJTVwZUSEVPUlkIVEhUUkVNVVMCVE8HVFVSS0lTSAJVQwNVS1ICVVADVVJQA1dHUwhXT01FTlNURAdXUklUSU5HB1lJRERJU0gVpQEAA0FBUwRBRVJPA0FMQQZBTUNVTFQHQU5BVE9NWQhBTlRIUkFSQwhBTlRIUkJJTwhBTlRIUkNVTAdBUFBQSFlTBkFSQUJBTQZBUkFCSUMEQVJDSAhBUk1FTklBTghBUlRTQURNTgVBU0lBTghBU0lBTkxBTghBU0lBTlBBTQVBU1RSTwJCQQNCQ1MCQkUGQklPSU5GCEJJT0xDSEVNB0JJT0xPR1kHQklPTUVERQdCSU9QSFlTB0JJT1NUQVQHQ0FUQUxBTgNDRUUDQ0hFBENIRU0DQ0lDA0NKUwZDTEFSQ0gFQ0xDSVYHQ0xJTUFURQZDTExJTkcIQ01QTFhTWVMGQ09HU0NJBENPTU0EQ09NUAdDT01QTElUA0NTUAVDWkVDSAVEQU5DRQdEQVRBU0NJB0RJR0lUQUwFRFVUQ0gFRUFSVEgDRUFTBEVDT04IRURDVVJJTlMHRURTUENIUgRFRFVDA0VFQgRFRUNTA0VIUwNFTEkHRU5HTElTSARFTkdSA0VOUwZFTlNDRU4HRU5WSVJPTgZGUkVOQ0gERlRWTQRHRU9HBkdFUk1BTgVHUkVFSwhHUkVFS01PRAdHVEJPT0tTBkhCRUhFRAZIRUJSRVcHSElTVEFSVAdISVNUT1JZBkhPTk9SUwJIUwZIVU1HRU4HSU5TVEhVTQdJTlRMU1REBklOVE1FRANJT0UFSVNMQU0HSVRBTElBTghKQVBBTkVTRQRKQVpaBkpVREFJQwVLUlNURARMQUNTBUxBVElOCExBVElOT0FNBExJTkcITUFDUk9NT0wETUFUSAdNQVRTQ0lFBE1DREIHTUVDSEVORwZNRUxBTkcETUVNUwVNRU5BUwNNRkcITUlDUkJJT0wHTUlERUFTVAZNSUxTQ0kHTVVTRVVNUwdNVVNJQ09MB01VU01FVEgITVVTVEhUUkUITkFUSVZFQU0GTkFWU0NJBE5FUlMITkVVUk9TQ0kETlVSUwhPUkdTVFVEWQNQQVQHUEVSU0lBTgRQSElMB1BIWVNJQ1MHUEhZU0lPTAZQT0xJU0gGUE9MU0NJBlBPUlRVRwNQUEUFUFNZQ0gGUFVCUE9MBFFNU1MGUkNBUlRTBVJDQVNMBlJDQ09SRQZSQ0hVTVMGUkNJRElWBlJDTEFORwZSQ05TQ0kGUkNTU0NJBVJFRUVTCFJFTElHSU9OB1JPTUxBTkcHUk9NTElORwdSVVNTSUFOA1NBUwVTQ0FORARTRUFTAlNJBlNMQVZJQwJTTQNTT0MFU1BBQ0UHU1BBTklTSARTU0VBBVNUQVRTB1NUREFCUkQIU1VSVk1FVEgCU1cGVEhFT1JZCFRIVFJFTVVTAlRPB1RVUktJU0gCVUMDVUtSAlVQA1VSUANXR1MIV09NRU5TVEQHV1JJVElORwdZSURESVNIFCsDpQFnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAQIFZAIJDxAPFgYfAwUGZGVwdGlkHwQFCmRlcHRfZGVzY3IfBWdkEBVkEFNlbGVjdCBhbiBvcHRpb24qIENvbGxlZ2Ugb2YgTGl0ZXJhdHVyZSwgU2NpZW5jZSAmIHRoZSBBcnRzLUNBVVAgVGF1Ym1hbiBDb2xsZWdlIG9mIEFyY2ggKyBVcmJhbiBQbGFubmluZxpDb0UgQmlvbWVkaWNhbCBFbmdpbmVlcmluZxhDb0UgQ2hlbWljYWwgRW5naW5lZXJpbmcnQ29FIENpdmlsIGFuZCBFbnZpcm9ubWVudGFsIEVuZ2luZWVyaW5nFUNvRSBDbGltYXRlIGFuZCBTcGFjZS9Db0UgRWxlY3RyaWNhbCBFbmdpbmVlcmluZyBhbmQgQ29tcHV0ZXIgU2NpZW5jZSpDb0UgRW52aXJvbm1lbnRhbCBTY2llbmNlcyBhbmQgRW5naW5lZXJpbmcpQ29FIEluZHVzdHJpYWwgYW5kIE9wZXJhdGlvbnMgRW5naW5lZXJpbmcqQ29FIE1hY3JvbW9sZWN1bGFyIFNjaWVuY2UgYW5kIEVuZ2luZWVyaW5nJUNvRSBNYXRlcmlhbHMgU2NpZW5jZSBhbmQgRW5naW5lZXJpbmcaQ29FIE1lY2hhbmljYWwgRW5naW5lZXJpbmcxQ29FIE51Y2xlYXIgRW5naW5lZXJpbmcgYW5kIFJhZGlvbG9naWNhbCBTY2llbmNlcxxDb0UgUHJvZ3JhbSBpbiBNYW51ZmFjdHVyaW5nG0NvRSBVbmRlcmdyYWR1YXRlIEVkdWNhdGlvbh5EaXZpc2lvbiBvZiBBbmF0b21pY2FsIFNjaWVuY2UXRGl2aXNpb24gb2YgS2luZXNpb2xvZ3kkTFNBIEFmcm9hbWVyaWNhbiBhbmQgQWZyaWNhbiBTdHVkaWVzFExTQSBBbWVyaWNhbiBDdWx0dXJlEExTQSBBbnRocm9wb2xvZ3kTTFNBIEFwcGxpZWQgUGh5c2ljcx5MU0EgQXNpYW4gTGFuZ3VhZ2VzICYgQ3VsdHVyZXMNTFNBIEFzdHJvbm9teQtMU0EgQmlvbG9neQ5MU0EgQmlvcGh5c2ljcw1MU0EgQ2hlbWlzdHJ5FUxTQSBDbGFzc2ljYWwgU3R1ZGllcxtMU0EgQ29tbXVuaWNhdGlvbiBhbmQgTWVkaWEaTFNBIENvbXBhcmF0aXZlIExpdGVyYXR1cmUTTFNBIENvbXBsZXggU3lzdGVtcxlMU0EgQ29tcHJlaGVuc2l2ZSBTdHVkaWVzIkxTQSBFYXJ0aCAmIEVudmlyb25tZW50YWwgU2NpZW5jZXMiTFNBIEVjb2xvZ3kgJiBFdm9sdXRpb25hcnkgQmlvbG9neQ1MU0EgRWNvbm9taWNzIUxTQSBFbmdsaXNoIExhbmd1YWdlICYgTGl0ZXJhdHVyZR5MU0EgRW5nbGlzaCBMYW5ndWFnZSBJbnN0aXR1dGUSTFNBIEV4aGliaXQgTXVzZXVtH0xTQSBGaWxtLCBUZWxldmlzaW9uLCBhbmQgTWVkaWEkTFNBIEdlcm1hbmljIExhbmd1YWdlcyAmIExpdGVyYXR1cmVzIkxTQSBHbG9iYWwgYW5kIEludGVyY3VsdHVyYWwgU3R1ZHkLTFNBIEhpc3RvcnkSTFNBIEhpc3Rvcnkgb2YgQXJ0CkxTQSBIb25vcnMYTFNBIEh1bWFuaXRpZXMgSW5zdGl0dXRlHkxTQSBJSTogR2xvYmFsIElzbGFtaWMgU3R1ZGllcy1MU0EgSUk6IEludGVybmF0aW9uYWwgYW5kIENvbXBhcmF0aXZlIFN0dWRpZXMYTFNBIElJOiBKYXBhbmVzZSBTdHVkaWVzLExTQSBJSTogTGF0aW4gQW1lcmljYW4gYW5kIENhcmliYmVhbiBTdHVkaWVzMExTQSBJSTogTWlkZGxlIEVhc3Rlcm4gYW5kIE5vcnRoIEFmcmljYW4gU3R1ZGllcyVMU0EgSUk6IE5hbSBDZW50ZXIgZm9yIEtvcmVhbiBTdHVkaWVzNExTQSBJSTogUnVzc2lhbiwgRWFzdCBFdXJvcGVhbiwgYW5kIEV1cmFzaWFuIFN0dWRpZXMYTFNBIElJOiBTLiBBc2lhbiBTdHVkaWVzGExTQSBJSTogU0UgQXNpYW4gU3R1ZGllcxJMU0EgSnVkYWljIFN0dWRpZXMPTFNBIExpbmd1aXN0aWNzD0xTQSBNYXRoZW1hdGljcxdMU0EgTWlkZGxlIEVhc3QgU3R1ZGllczJMU0EgTW9sZWN1bGFyLCBDZWxsdWxhciwgYW5kIERldmVsb3BtZW50YWwgQmlvbG9neRpMU0EgT3JnYW5pemF0aW9uYWwgU3R1ZGllcw5MU0EgUGhpbG9zb3BoeQtMU0EgUGh5c2ljcxVMU0EgUG9saXRpY2FsIFNjaWVuY2UOTFNBIFBzeWNob2xvZ3kvTFNBIFF1YW50aXRhdGl2ZSBNZXRob2RzIGluIHRoZSBTb2NpYWwgU2NpZW5jZXMXTFNBIFJlc2lkZW50aWFsIENvbGxlZ2UjTFNBIFJvbWFuY2UgTGFuZ3VhZ2VzICYgTGl0ZXJhdHVyZXMiTFNBIFNsYXZpYyBMYW5ndWFnZXMgJiBMaXRlcmF0dXJlcw1MU0EgU29jaW9sb2d5DkxTQSBTdGF0aXN0aWNzF0xTQSBTdHVkaWVzIGluIFJlbGlnaW9uHExTQSBTd2VldGxhbmQgV3JpdGluZyBDZW50ZXIaTFNBIFVHOiBDdXJyaWN1bHVtIFN1cHBvcnQeTFNBIFdvbWVuJ3MgYW5kIEdlbmRlciBTdHVkaWVzEk1FRCBCaW9pbmZvcm1hdGljcxhNRUQgQmlvbG9naWNhbCBDaGVtaXN0cnkSTUVEIEh1bWFuIEdlbmV0aWNzFU1FRCBJbnRlcm5hbCBNZWRpY2luZR9NRUQgTWljcm9iaW9sb2d5IGFuZCBJbW11bm9sb2d5KE1FRCBNb2xlY3VsYXIgYW5kIEludGVncmF0aXZlIFBoeXNpb2xvZ3kbTUVEIE5ldXJvc2NpZW5jZSBMYWJvcmF0b3J5KU1PRVA6IEFpciBGb3JjZSBPZmZpY2VyIEVkdWNhdGlvbiBQcm9ncmFtJE1PRVA6IEFybXkgT2ZmaWNlciBFZHVjYXRpb24gUHJvZ3JhbSRNT0VQOiBOYXZ5IE9mZmljZXIgRWR1Y2F0aW9uIFByb2dyYW0MTXVzaWMgU2Nob29sDE11c2ljOiBEYW5jZRhNdXNpYzogVGhlYXRyZSBhbmQgRHJhbWESUmVnaXN0cmFyJ3MgT2ZmaWNlF1Jvc3MgU2Nob29sIG9mIEJ1c2luZXNzE1NjaG9vbCBvZiBFZHVjYXRpb24VU2Nob29sIG9mIEluZm9ybWF0aW9uEVNjaG9vbCBvZiBOdXJzaW5nFVNjaG9vbCBvZiBTb2NpYWwgV29yax5TTkUgUHJvZ3JhbSBpbiB0aGUgRW52aXJvbm1lbnQvU05FIFNjaG9vbCBvZiBOYXR1cmFsIFJlc291cmNlcyBhbmQgRW52aXJvbm1lbnQcU1BIIEJpb3N0YXRpc3RpY3MgRGVwYXJ0bWVudCFTUEggRW52aXJvbm1lbnRhbCBIZWFsdGggU2NpZW5jZXMoU1BIIEhlYWx0aCBCZWhhdmlvciBhbmQgSGVhbHRoIEVkdWNhdGlvbitTUFA6IEdlcmFsZCBSLiBGb3JkIFNjaG9vbCBvZiBQdWJsaWMgUG9saWN5GFNSQy1QU00gR3JhZHVhdGUgUHJvZ3JhbRVkAAYxNzAwMDAGMzcyMTAwBjIxMDYwMAYyMTMwMDAGMjE1MDAwBjIyNDAwMAYyMTYwMDAGMjExNTAwBjIyMTAwMAYyMTEwMzAGMjIxODAwBjIyMjUwMAYyMjcwMDAGMjEwNzAwBjIxMDQwMAYyNTg2MDAGNDUwMDAwBjE5MDMwMAYxOTMwMDAGMTcyMDAwBjE4NDYwMAYxNzYwMDAGMTcyNTAwBjE4ODkwMAY1NTQwMDAGMTczNTAwBjE3NDAwMAYxODgzMDAGMTkxNDAwBjU1MDQwMAYxOTEyMDAGMTc3MDAwBjE4OTEwMAYxNzUwMDAGMTc1NTAwBjE4MTUwMAYyMDEwMDAGMTkxNjAwBjE3ODAwMAYxNzE1MDAGMTc5MDAwBjE3OTUwMAYxODAwMDAGMTcxMTAwBjE5MjYwMAYxOTM3MDAGMTkyMDAwBjE5NTEwMAYxOTI1MDAGMTk0MzAwBjE5NDAwMAYxOTQ0MDAGMTk0NTAwBjE3OTEwMAYxODEyMDAGMTgzMDAwBjE4MzUwMAYxODkwMDAGMTc0NzAwBjE4NDAwMAYxODQ1MDAGMTg1MDAwBjE4NTUwMAYxNzUzMDAGMTg2MDAwBjE4NjUwMAYxODcwMDAGMTg3NTAwBjE4ODUwMAYxOTQ3MDAGMTc1NjAwBjE3MTkwMAYxODg3MDAGMjMxMzUwBjIzNDAwMAYyMzYwMDAGMjM3MDAwBjI0NTAwMAYyNTcwMDAGMzA3MDAwBjQxNjAwMAY0MTcwMDAGNDE4MDAwBjQyMDAwMAY0MzE1MDAGNDMzMDAwBjUxNzUwMAYzODAwMDAGNDA1MDAwBjQxNTAwMAY0NDAwMDAGNDY1MDAwBjQzNTMxMAY0MzUwMDAGNDU2MDAwBjQ1NzUwMAY0NTgzMDAGNDY0MDAwBjU4NTE1NBQrA2RnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnFgFmZAIJDw8WAh4HVmlzaWJsZWhkFgICCw88KwAJAGQCDw8PFgIfBmhkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUmY3RsMDAkQ29udGVudFBsYWNlSG9sZGVyMSRjaGJTaG93RGVzY3IFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY2hiU2hvd0NHVGVybXMLPJlKjRjpX/BVyHm2DcAOgY9nBQ==',
        '__VIEWSTATEGENERATOR': '2D833CB4',
        '__EVENTVALIDATION': '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'
        }

        response = requests.post('https://webapps.lsa.umich.edu/CrsMaint/Public/CB_PublicBulletin.aspx', headers=headers, params=params, data=data)



        tables = soup(response.text, "html.parser").find_all("td", {"valign": "top"})
        for table in tables:
            try:
                _title = table.find("b").getText(strip=True)
                _course_info = " ".join(table.find("i").text.split())
                _desc = table.find("p").getText(strip=True)
                _urls = [f"{a.text.strip()} - {a['href']}" for a in table.find_all("a")]
                
                course = Course(title=_title, 
                                info=_course_info, 
                                desc=_desc, 
                                urls=_urls, 
                                listing=_listing)
                course.save()

                print(''*100)
                print(_title)
                print("-" * 120)
            except AttributeError:
                continue
    return render(request, "courses/courses_home.html")