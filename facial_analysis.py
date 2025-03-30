from deepface import DeepFace
import cv2
import threading
import queue
import time

#TODO
# maybe use json, maybe use dictionary

def analyze_face(shared_queue, f_input):

    while True:
        status, frame = f_input.read()

        #if no frame was captured, skip processing, move to next frame
        if (not status):
            continue 

        try:
            #Get emotion data
            analysis_result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            emotion = analysis_result[0]['dominant_emotion']
            confidence = analysis_result[0]['emotion'][emotion]

        except:
            emotion = "could not detect emotion"
            confidence = 0.0

        #create dictionary of emotion data, place into pipeline
        emotion_data = {"emotion" : emotion, "confidence" : confidence}

        shared_queue.put(emotion_data)

        time.sleep(1)

    facial_input.release()
    

def display_camera_feed(f_input):
    while True:
        
        status, frame = f_input.read()

        if (not status):
            break

        cv2.imshow("Face", frame)

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    f_input.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pass

