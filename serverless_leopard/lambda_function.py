import base64
import cgi
import io
import json
import logging
import os
import uuid

import pvleopard

log = logging.getLogger()
log.setLevel(logging.INFO)

# create at global scope
handle = pvleopard.create(access_key=os.environ['ACCESS_KEY'])


def lambda_handler(event, context):
    # change multipart/form-data to file
    fp = io.BytesIO(base64.b64decode(event['body']))
    _, pdict = cgi.parse_header(event['headers']['Content-Type'])
    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')

    form_data = cgi.parse_multipart(fp, pdict)
    audio_data = form_data['audio_file'][0]
    log.info(f"Retrieved audio data with boundary: {pdict['boundary']}, audio length: {len(audio_data)}")

    temp_file = f'/tmp/{str(uuid.uuid4())}'
    with open(temp_file, 'wb') as f:
        f.write(audio_data)
    log.info(f"Audio data saved at: {temp_file}")
    
    # leopard stt
    transcription = handle.process_file(temp_file)
    log.info(f"Process complete, transcription: {transcription}")
    
    # clean up
    os.remove(temp_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'transcription': transcription
        })
    }
