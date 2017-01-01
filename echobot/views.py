from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextMessage,TextSendMessage

from urllib.request import urlopen
import xml.etree.ElementTree as ET

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

cities = ["臺北","新北","桃園","臺中","臺南","高雄","基隆","新竹縣","新竹市","苗栗","彰化","南投","雲林","嘉義縣","嘉義市","屏東","宜蘭","花蓮","臺東","澎湖","金門","連江"]

def retrieve_data(place):
        url = 'http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey={API_KEY}'.format(API_KEY=settings.API_KEY) 
        filehandle = urlopen(url)
        tree = ET.parse(filehandle)
        root = tree.getroot()

        for node in root.iterfind('.//{urn:cwb:gov:tw:cwbcommon:0.1}location'):
                if place in node[0].text:
                        weather = node.find('.//{urn:cwb:gov:tw:cwbcommon:0.1}parameterName')
                        return node[0].text + weather.text

@csrf_exempt
def callback(request):
	if request.method == 'POST':
		signature = request.META['HTTP_X_LINE_SIGNATURE']
		body = request.body.decode('utf-8')

		try:
			events = parser.parse(body,signature)
		except InvalidSignatureError:
			return HttpResponseForbidden()
		except LineBotApiError:
			return HttpResponseBadRequest()

		find = 0
		for event in events:
			if isinstance(event,MessageEvent):
				if isinstance(event.message,TextMessage):
					if "天氣" in event.message.text:
						for city in cities:
							if city in event.message.text:
								reply = retrieve_data(city)
								find = 1
								break
						if find == 0:
							reply = retrieve_data("臺南")
					else:
						reply = event.message.text
					line_bot_api.reply_message(
                    	event.reply_token,
                        TextSendMessage(text=reply)
                    )


		return HttpResponse()
	else:
		return HttpResponseBadRequest()
