import boto3

def lambda_handler(event, context):
    session = boto3.Session(aws_access_key_id="ASIARVAB6G2YZPGBR2GQ",
                            aws_secret_access_key="wD+W0LvQbgMlL2989t3uS+xBakN/DpSBjUZlIR98",
                            aws_session_token="FwoGZXIvYXdzEMb//////////wEaDElJBZ6UCG0QQ5hVSyLAAVZERrH0zRxwVW0R5eqa/KQTviPxVH00BQXHeqE9z9N1N0GtMEQwhFKO23bKvyP8PVpaDK4u3YzThn3bidt7LUdSFlCRDzMxzHcvrUsOM4D1iSPFUOmvE6dAlgzXf3IGdfZG+u2apYNLDD7ZP6VPwBNNLwhpHbVaGJuVV5Z77Gk32C1gmbp2JFKUizC7v4kcKI++J5lYs6BZeWMiRomPR7M8jKh9+Ani9vPzYZlGoausbcs6yjJsiJ0RqRnv6UZc/CjF46KSBjIt1G7sJEyvqqQXybECMalBpLGkyihtYQf+DnQqL6QOjoW5tGNQH/S/NENFKmto",
                            region_name='us-east-1'
                            )
    translate = session.client(service_name='translate', use_ssl=True)
    result = translate.translate_text(Text=event['text'],
                                      SourceLanguageCode="en", TargetLanguageCode=event['language'])
    polly = session.client(service_name='polly', use_ssl=True)
    if event['language'] == "hi":
        voiceId = 'Aditi'
        languageCode = 'hi-IN'
    elif event['language'] == "fr-CA":
        voiceId = 'Chantal'
        languageCode = 'fr-CA'
    elif event['language'] == "ar":
        voiceId = 'Zeina'
        languageCode = 'arb'
    elif event['language'] == "it":
        voiceId = 'Carla'
        languageCode = 'it-IT'
    elif event['language'] == "de":
        voiceId = 'Marlene'
        languageCode = 'de-DE'
    audio = polly.start_speech_synthesis_task(Text=result.get('TranslatedText'),
                                            LanguageCode=languageCode,
                                                VoiceId=voiceId,
                                                OutputFormat='mp3',
                                                Engine="standard",
                                                TextType='text',
                                                SampleRate='8000',
                                                OutputS3BucketName='greencloudproject',
                                                OutputS3KeyPrefix="greenclouduser"
                                                )
    object_name = audio['SynthesisTask']['OutputUri']
    print(object_name)
    startIndex = object_name.find('greenclouduser')
    keyName = object_name[startIndex: len(object_name)]
    print(keyName)
    s3 = session.client('s3')
    resp = s3.generate_presigned_url('get_object',
                            Params={'Bucket': 'greencloudproject',
                            'Key': keyName},
                            ExpiresIn=100000) 
    return str(resp)