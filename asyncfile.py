from logging import critical
import pymongo
from asyncio_mqtt.client import Client,MqttError
import json
import asyncio
from datetime import datetime,timedelta
# from send_notification import send_notification
from env_vars import env
from logger.log import get_logger
logger = get_logger()


try:
    conn = pymongo.MongoClient(env.mongodb_localhost)
    db = conn.StoreRealTimeData
    logger.info("Coonection Successful to database :%s" % (env.mongodb_localhost))
except Exception as e:
    logger.error("Exception caught While connection Database: %s" % e)


async def MqttConnect(sendNotificationTime):
    try:
        list = []
        async with Client(env.mqtt_broker, env.mqtt_port) as client:
            logger.info("Conection Successful to Mqtt Broker :%s with port :%s" % (env.mqtt_broker,env.mqtt_port))
            async with client.filtered_messages('#') as messages:
                try:
                    await client.subscribe('#')
                except Exception as e:
                    logger.error("Exception caught While Subscribe to Topic: %s" % e)
                async for message in messages:
                    cTime = datetime.now()
                    try:
                        # print("Message",message.payload.decode())
                        Temp = json.loads(message.payload.decode())['temp']
                        Organization = json.loads(message.payload.decode())['org']
                        Device_ID = json.loads(message.payload.decode())['d_id']
                        Freeze_ID = json.loads(message.payload.decode())['f_id']
                        # print("Info",Temp,Organization,Device_ID,Freeze_ID)
                
                        collections = db.list_collection_names()  
                        list = []
                        if Organization not in collections:
                            db.create_collection(Organization)

                        list.append({
                            "metadata": {"device_name": Device_ID, "freeze_id": Freeze_ID, "type": "temperature"},
                            "timestamp": datetime.today().replace(microsecond=0),
                            "temp": Temp,
                        })
                        db[Organization].insert_many(list)
                        isCrtical = json.loads(message.payload.decode())["critical"]
                        # if isCrtical:
                        #     print("critical Temperature")
                        #     kwargs={'organization': Organization, 'freeze_id': Freeze_ID, 'device_id': Device_ID}
                        #     if cTime.strftime("%d/%m/%Y %H:%M") == sendNotificationTime.strftime("%d/%m/%Y %H:%M"):
                        #         print("Sending notification after 5 min...")
                        #         sendNotificationTime = cTime + timedelta(minutes=env.time_interval_to_send_sms)                       
                        #         print("Is critical after 1 min...")
                        #         await send_notification(kwargs, message)
                        #     print("End critical temperature")
                    except:
                        pass
    except Exception as e:
            logger.error("Exception caught While connection MqttBroker: %s" % e)


async def main():
    reconnect_interval = 3 
    while True:
        try:
            current_time = datetime.now()
            sendNotificationTime = current_time
            await MqttConnect(sendNotificationTime)
        except MqttError as error:
            print(f'Error "{error}". Reconnecting in {reconnect_interval} seconds.')
        finally:
            await asyncio.sleep(reconnect_interval)


asyncio.run(main())


