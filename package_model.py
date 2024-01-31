class Package:
    def __init__(self, package_id, receiver_e, sender_e, target):
        self.package_uid = package_id
        self.receiver_email = receiver_e
        self.sender_email = sender_e
        self.target_parcel_locker = target

    def getId(self):
      return self.package_uid
    
    def getTarget(self):
      return self.target_parcel_locker
    
    def __str__(self):
        return f"Package ID: {self.package_uid}, Receiver: {self.receiver_email}, Sender: {self.sender_email}, Target Parcel Locker: {self.target_parcel_locker}"

