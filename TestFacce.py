import face_recognition
import os
import cv2

KNOWN_FACES_DIR = 'known_faces'
UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = .5 #higher = more matches but more error
FRAME_THICKNESS = 2
FONT_THICKNESS = 2
MODEL = 'cnn' #or hog

print('Loading known faces...')

known_faces = []
known_names = []

for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        
        if len(face_recognition.face_encodings(image)) > 0:
            print('face detected')
            encoding = face_recognition.face_encodings(image)[0]
        #encoding = face_recognition.face_encodings(image)
        #if len(encoding) > 0 :
        #    encoding = encoding[0]
        #else:
        #    print("no face found")

        # Append encodings and name
            known_faces.append(encoding)
            known_names.append(name)


print('Processing unknown faces...')

for filename in os.listdir(UNKNOWN_FACES_DIR):

    print(f'Filename {filename}', end='')
    image = face_recognition.load_image_file(f'{UNKNOWN_FACES_DIR}/{filename}')

    locations = face_recognition.face_locations(image, model=MODEL)

    encodings = face_recognition.face_encodings(image, locations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    print(f', found {len(encodings)} face(s)')
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f' - {match} from {results}')
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = [0,255,0]

            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)

            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), FONT_THICKNESS)

    # Show image
    cv2.imshow(filename, image)
    cv2.waitKey(10000)
    #cv2.destroyWindow(filename)