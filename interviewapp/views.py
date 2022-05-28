import json
import threading
from datetime import time
import os

from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models import Max
from django.shortcuts import render
from interviewapp.models import Question, Result

from interviewapp.tasks import result



# Create your views here.
# def ThresView(request):
#     if request.method == 'GET':
#         return render(request, 'interviewapp/threshold.html')
#     else:
#         print(request.POST)
#         global threshold
#         threshold = int(request.POST['threshold'])
#         return render(request, 'interviewapp/threshold.html')



def QuestionView(request):
    if request.method == 'GET':
        corp_name = request.GET.get('corp', None)
        dept_name = request.GET.get('dept', None)
        quest_id = request.GET.get('question', None)
        next_id = str(int(quest_id) + 1)
        question = Question.objects.filter(quest_id=quest_id)
        quest_level = str(question[0].level) if len(question) != 0 else '1'
        result = Result.objects.filter(user_id=request.user)
        if len(result) == 0:
            report_num = 1
        else:
            max_num = result.aggregate(report_num=Max('report_num'))['report_num']
            max_result = Result.objects.filter(user_id=request.user, report_num=max_num)
            if len(max_result) >= 7:
                report_num = max_num + 1
            elif quest_id == '1':
                max_result.delete()
                report_num = max_num
            else:
                report_num = max_num
        context = {
            'question': question,
            'corp_name': corp_name,
            'dept_name': dept_name,
            'next_id': next_id,
            'quest_id': quest_id,
            'quest_level': quest_level,
            'report_num': report_num
        }
        if (quest_level == '3'):
            return render(request, 'interviewapp/tendency.html', context)
        else:
            return render(request, 'interviewapp/question.html', context)



def ResultView(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        quest = Question.objects.get(quest_id=request.POST['quest_id'])
        result_flag = Result.objects.filter(user_id=user, report_num=request.POST['report_num'], quest_id=quest).exists()
        if request.POST['quest_level'] != '3':
            if not result_flag:
                file = request.FILES['file']
                fname = file.name
                fs = FileSystemStorage(location='media/webm/')
                filename = fs.save(fname, file)
                new_fname = f"{request.user}_{request.POST['report_num']}_{request.POST['quest_id']}"
                os.system(f"ffmpeg -y -i media/webm/{filename} media/mp4/{new_fname}.mp4")
                os.system(f"ffmpeg -y -i media/webm/{filename} media/wav/{new_fname}.wav")
                os.remove(f"media/webm/{filename}")
                result.delay(new_fname, request.user.username, request.POST['quest_id'], request.POST['report_num'], request.POST['corp_name'], request.POST['dept_name'])
        else:
            if not result_flag:
                tendency = request.POST.getlist('tendency')
                str_tendency = ', '.join(tendency)
                Result.objects.create(user_id=user, report_num=request.POST['report_num'], quest_id=quest, result_add=str_tendency)

        return render(request, 'interviewapp/question.html')



def ReportView(request):
    if request.method == 'GET':
        result = Result.objects.filter(user_id=request.user)
        if len(result) == 0:
            return render(request, 'homeapp/home.html')
        else:
            max_num = result.aggregate(report_num=Max('report_num'))['report_num']
            max_result = Result.objects.filter(user_id=request.user, report_num=max_num)
            max_count = max_result.count()
            if max_count < 7:
                max_result.delete()
            # result = Result.objects.filter(user_id=request.user)
            result = Result.objects.filter(user_id=request.user).order_by('report_num', 'quest_id')
            context = {
                'result_list': result,
            }
            return render(request, 'homeapp/home.html', context)



# def SettingView(request):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#
#     detector_params = cv2.SimpleBlobDetector_Params()
#     detector_params.filterByArea = True
#     detector_params.maxArea = 1500
#     detector = cv2.SimpleBlobDetector_create(detector_params)
#
#     cap = cv2.VideoCapture('http://127.0.0.1:8000/thres/')  # 웹캠 사용(아직 안됨)
#     # cv2.createTrackbar('threshold', 'image', 0, 255, nothing)
#
#     while True:
#         _, frame = cap.read()
#         face_frame = detect_faces(frame, face_cascade)
#         if face_frame is not None:
#             eyes = detect_eyes(face_frame, eye_cascade)
#             for eye in eyes:
#                 if eye is not None:
#                     # threshold = cv2.getTrackbarPos('threshold', 'image')
#                     threshold = 35
#                     eye = cut_eyebrows(eye)
#                     # keypoints = blob_process(eye, threshold, detector)
#                     keypoints = blob_process(eye, threshold, detector)
#                     print(keypoints)
#                     eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255),
#                                             cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#         cv2.imshow('image', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     cap.release()
#
#     return render(request, 'interviewapp/threshold.html', {'cap': cap, })