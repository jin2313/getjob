from __future__ import absolute_import, unicode_literals
from celery import shared_task

import json
import cv2
import imutils
import speech_recognition as sr
import numpy as np
from django.contrib.auth.models import User

from keras.models import load_model
from tensorflow.keras.utils import img_to_array

from interviewapp.models import Question, Result



@shared_task
def result(filename, username, quest_id, report_num, corp_name, dept_name):
    text = speech_to_text(f'media/wav/{filename}.wav')
    feelings_faces = expression_recognition(f'media/mp4/{filename}.mp4')
    total, good = eye_tracking(f'media/mp4/{filename}.mp4')
    face_total = feelings_faces['negative'] + feelings_faces['positive'] + feelings_faces['neutral']
    if feelings_faces['neutral'] - 100 > 0 and feelings_faces['positive'] + 100 < face_total:
        feelings_faces['neutral'] -= 100
        feelings_faces['positive'] += 100
    elif feelings_faces['neutral'] - 70 > 0 and feelings_faces['positive'] + 70 < face_total:
        feelings_faces['neutral'] -= 70
        feelings_faces['positive'] += 70
    elif feelings_faces['neutral'] - 50 > 0 and feelings_faces['positive'] + 50 < face_total:
        feelings_faces['neutral'] -= 50
        feelings_faces['positive'] += 50
    feelings_faces = json.dumps(feelings_faces)
    eye_rate = round(good / total * 100, 2) if total != 0 else 0
    user = User.objects.get(username=username)
    quest = Question.objects.get(quest_id=quest_id)
    if quest_id == "2":
        count = count_talent(text, corp_name)
        Result.objects.create(user_id=user, report_num=report_num, quest_id=quest, result_stt=text,
                              result_eye=eye_rate, result_face=feelings_faces, result_add=count)
    elif quest_id == "3":
        count = count_job(text, dept_name)
        Result.objects.create(user_id=user, report_num=report_num, quest_id=quest, result_stt=text,
                              result_eye=eye_rate, result_face=feelings_faces, result_add=count)
    else:
        Result.objects.create(user_id=user, report_num=report_num, quest_id=quest, result_stt=text,
                              result_eye=eye_rate, result_face=feelings_faces)



def speech_to_text(file_path):
    r = sr.Recognizer()
    harvard = sr.AudioFile(file_path)
    with harvard as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
        except:
            text = '내용이 없습니다.'
    return text



def expression_recognition(file_path):
    # hyper-parameters for bounding boxes shape
    # loading models
    face_detection = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    emotion_classifier = load_model('model/expression_recognition.hdf5', compile=False)   # 경로 너걸로 바꿔줘!
    EMOTIONS = ['angry', 'disgust', 'scared', 'happy', 'sad', 'surprised', 'neutral']

    # feelings_faces = []
    # feelings_faces = {'angry': 0, 'disgust': 0, 'scared': 0,
    #                   'happy': 0, 'sad': 0, 'surprised': 0, 'neutral': 0}
    feelings_faces = {"negative": 0, "neutral": 0, "positive": 0}
    # for index, emotion in enumerate(EMOTIONS):
    # feelings_faces.append(cv2.imread('emojis/' + emotion + '.png', -1))

    # starting video streaming
    camera = cv2.VideoCapture(file_path)  # 녹화된 영상
    while True:
        ret, frame = camera.read()
        if ret:
            # reading the frame
            frame = imutils.resize(frame, width=300)  # your_face 창 사이즈 조절
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # your_face 창 흑백으로 바꿈
            faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            canvas = np.zeros((250, 300, 3), dtype="uint8")
            frameClone = frame.copy()
            if len(faces) > 0:
                faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                (fX, fY, fW, fH) = faces
                # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                # the ROI for classification via the CNN
                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                preds = emotion_classifier.predict(roi)[0]
                emotion_probability = np.max(preds)
                label = EMOTIONS[preds.argmax()]
                # feelings_faces.append(label)
                # negative = ('angry', 'disgust', 'scared', 'sad')
                positive = ('happy')
                neutral = ('surprised', 'neutral')
                if label in positive:
                    feelings_faces['positive'] += 1
                elif label in neutral:
                    feelings_faces['neutral'] += 1
                else:
                    feelings_faces['negative'] += 1
                # feelings_faces[label] += 1
            else:
                continue
        else:
            break

        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            # construct the label text
            text = "{}: {:.2f}%".format(emotion, prob * 100)

            # draw the label + probability bar on the canvas
            # emoji_face = feelings_faces[np.argmax(preds)]

            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
            cv2.putText(frameClone, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
        #    for c in range(0, 3):
        #        frame[200:320, 10:130, c] = emoji_face[:, :, c] * \
        #        (emoji_face[:, :, 3] / 255.0) + frame[200:320,
        #        10:130, c] * (1.0 - emoji_face[:, :, 3] / 255.0)

    # print(feelings_faces)
    camera.release()
    cv2.destroyAllWindows()

    return feelings_faces



def eye_tracking(file_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    detector_params = cv2.SimpleBlobDetector_Params()
    detector_params.filterByArea = True
    detector_params.maxArea = 1500
    detector = cv2.SimpleBlobDetector_create(detector_params)

    cap = cv2.VideoCapture(file_path)
    keypoint_list = []
    good = 0

    while True:
        ret, frame = cap.read()
        if ret:
            face_frame = detect_faces(frame, face_cascade)
            if face_frame is not None:
                eyes = detect_eyes(face_frame, eye_cascade)
                for eye in eyes:
                    if eye is not None:
                        # threshold = cv2.getTrackbarPos('threshold', 'image')
                        threshold = 35   # 전달 받은 threshold 값 넣어주기(일단 내 방 조명에 맞춰 설정한거임)
                        eye = cut_eyebrows(eye)
                        keypoints = blob_process(eye, threshold, detector)

                        if len(keypoints) != 0:
                            good += 1
                        keypoint_list.append(keypoints)

                        eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255),
                                                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        else:
            break

    good += 20 if len(keypoint_list) >= good + 20 else len(keypoint_list) - (good + 5) # 사람은 1분에 평균 20회 정도 눈을 깜박인다고 함
    # print(len(keypoint_list), good)
    cap.release()

    return len(keypoint_list), good



def detect_faces(img, face_cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]

    return frame



def detect_eyes(img, eye_cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None

    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]

    return left_eye, right_eye



def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img



def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)

    return keypoints



def count_talent(stt_text, corp_name):
    naver = ['동료', '영향', '성장', '데이터', '흐름', '설득', '경험', '해석', '커뮤니케이션', '창의', '소통']
    ncsoft = ['진지', '헌신', '감동', '전문성', '도전', '창의', '열정', '실행력', '협력', '다양']

    s = stt_text.split()  # 공백 기준으로 분리
    talent = []

    if (corp_name == 'NAVER'):   # 네이버
        for i in s:
            for j in naver:
                if j in i:
                    talent.append(i)
    elif (corp_name == 'NCSOFT'):   # 엔씨소프트
        for i in s:
            for j in ncsoft:
                if j in i:
                    talent.append(i)

    return {corp_name: len(talent)}   # 인재상 포함된 단어 말한 횟수? 반환, 단어 자체를 반환하려면 talent 리스트 반환하면 됨



def count_job(stt_text, dept_name):
    app = ['안드로이드', '아이오에스', '아이폰', '앱', '스위프트', '소켓', '배포', '플레이스토어', '자바', '코틀린', '엑스코드', '그래들']
    bigdata = ['파이썬', '빅데이터', '데이터', '판다스', '시각화', '핸들링', '전처리', '통계', '회귀', '데이터프레임', '수집']
    be = ['리액트', '스프링', '에이더블유에스', 'aws', 'AWS', '웹', '장고', '노드제이에스', '서버', '배포', '아키텍처', '에이피아이', 'API', 'api', '프레임워크']
    qa = ['관리', '종합', '통계', '경영', '품질', '게임', '큐에이', '비용', '형상', '리스크', '검증', '테스트']
    icon = ['디자인', '아이콘', '패키지', '영상', '정보', '일러스트레이터', '포토샵', '스케치', '시각']
    text = ['자연어', '버트', '지피티', '처리', '토큰화', '모델', '트랜스포머', '분류', '벡터', '파인튜닝', '파이토치', '파이썬']

    s = stt_text.split()  # 공백 기준으로 분리
    job = []

    # 네이버
    if (dept_name == 'iOS/Android 개발자'):
        for i in s:
            for j in app:
                if j in i:
                    job.append(i)
    elif (dept_name == '빅데이터 분석 엔지니어'):
        for i in s:
            for j in bigdata:
                if j in i:
                    job.append(i)
    elif (dept_name == 'Back-end 개발자'):
        for i in s:
            for j in be:
                if j in i:
                    job.append(i)

    # 엔씨소프트
    elif (dept_name == 'PC 온라인 게임 QA'):
        for i in s:
            for j in qa:
                if j in i:
                    job.append(i)
    elif (dept_name == '아이콘 디자이너'):
        for i in s:
            for j in icon:
                if j in i:
                    job.append(i)
    elif (dept_name == '텍스트 처리 개발자'):
        for i in s:
            for j in text:
                if j in i:
                    job.append(i)

    return {dept_name: len(job)}  # 인재상 포함된 단어 말한 횟수? 반환, 단어 자체를 반환하려면 talent 리스트 반환하면 됨