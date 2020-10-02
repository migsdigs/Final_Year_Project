#File to link the video display with the controls


class Controller():
    def __init__(self):
        self.video_frame = None
        self.controls_frame = None

        self.inspection_time_limit_flag = False     #flag state determines if inspection time limit is going to be used or not
        self.reference_image_delay_flag = False     #flag state determines if reference image delay is going to be used or not
        self.frame_capture_interval_flag = False    #flag state determines if frames saving at a set interval is going to be used or not
        self.reference_image_taken_flag = True      #flag state indicates whether the reference image has been taken or not
        self.save_count = 0
        self.interval_save_count = 0

        #set the reference image delay, frame capture interval & inspection time limit to 0 default (used as a check condition later)
        self.reference_image_delay = 0
        self.frame_capture_interval = 0
        self.inspection_time_limit = 0

        self.save_location = str()
        self.save_location_flag = False
    
    ######################## METHODS FOR SETTING FRAMES TO CONTROL ########################
    
    def set_video_frame(self, frame):   #assign the video_frame class from the DS_GUI class to the video_frame object of the controller (allows for methods from video_frame class to be called in controller)
        self.video_frame = frame

    def set_controls_frame(self, frame):
        self.controls_frame = frame
    
    def set_setup_frame(self, frame):
        self.setup_frame = frame


    ######################## METHODS FOR VIDEO CONTROL ########################

    def pause(self):    #method for pausing video
        self.video_frame.pause_video()  #executes the pause_video() method from thee video frame class when pause() method is called
        self.controls_frame.pause_button["state"] = "disabled"
        self.controls_frame.play_button["state"] = "enabled"
        self.controls_frame.stop_button["state"] = "enabled"
        #print("video paused")
    
    def play(self):     #method to play cideo
        self.video_frame.play_video()
        self.controls_frame.play_button["state"] = "disabled"
        self.controls_frame.pause_button["state"] = "enabled"
        self.controls_frame.stop_button["state"] = "disabled"
        #print("video played")
    
    def stop(self):     #method to stop video/inspection
        self.video_frame.stop_video()
        self.controls_frame.play_button["state"] = "disabled"
        self.controls_frame.pause_button["state"] = "disabled"
        self.controls_frame.stop_button["state"] = "disabled"
        #print("video stopped")

    
    def display_fringes(self):  #display fringes when fringe display button is pressed
        self.video_frame.display_fringes_flag = True
        self.controls_frame.fringe_pattern_button["state"] = "disabled"
        self.controls_frame.real_time_video_button["state"] = "enabled"
    

    def display_video(self):    #display real time video when video button is pressed
        self.video_frame.display_fringes_flag = False
        self.controls_frame.fringe_pattern_button["state"] = "enabled"
        self.controls_frame.real_time_video_button["state"] = "disabled"


    ######################## METHODS FOR IMAGES & SAVING ########################
  
    def save_snapshot(self):    #method to save images when snapshot button is hit
        snapshot_name = "snapshot"+str(self.save_count)+".jpeg"
        self.video_frame.img.save(snapshot_name)
        self.save_count = self.save_count+1


    def save_ref_image(self):   #method to save the reference image once it is taken
        self.video_frame.ref_img.save("reference_image.jpeg")


    def frame_capture_save(self):    #method to save images at set intervals
        frame_capture_interval_milliseconds = self.frame_capture_interval*1000

        if self.frame_capture_interval_flag:
            if self.frame_capture_interval > 0: #checking that the interval (seconds) set is valid
            
                frame_capture_name = "interval_capture"+str(self.interval_save_count)+".jpeg"
                self.video_frame.img.save(frame_capture_name)
                print("saved frame")
                self.interval_save_count = self.interval_save_count+1
                self.setup_frame.start_inspection_button.after(frame_capture_interval_milliseconds, lambda: self.frame_capture_save())            


    def get_save_location(self):
        self.save_location = self.controls_frame.folder_directory.get()
        self.save_location_flag = True
        

    ######################## METHODS FOR START INSPECTION ########################

    def start(self):
        self.controls_frame.pause_button["state"] = "enabled"

        self.setup_frame.inspection_time_limit_check_button["state"] = "disabled"
        self.setup_frame.inspection_time_limit_set_button["state"] = "disabled"

        self.setup_frame.frame_capture_interval_check_button["state"] = "disabled"
        self.setup_frame.frame_capture_interval_check_button["state"] = "disabled"

        self.setup_frame.reference_image_delay_check_button["state"] = "disabled"
        self.setup_frame.reference_image_delay_set_button["state"] = "disabled"

        self.setup_frame.start_inspection_button["state"] = "disabled"

        self.controls_frame.snapshot_button["state"] = "enabled"

        self.reference_image()      #call take_reference_image method
        self.frame_capture_save()   #call frame_capture_save
        self.inspection_limit()     #call inspection_limit method

        
    def reference_image(self):     #determines when reference image will be taken, then takes reference image using take_reference_image method
        if not self.reference_image_delay_flag:     #if reference image delay flag is False, a reference image will be taken immediately after start
            self.take_reference_image()

        elif self.reference_image_delay_flag:       #if reference image delay flag is true, reference image will only be taken after x seconds    
            if self.reference_image_delay > 0:
                reference_image_delay_milliseconds = self.reference_image_delay*1000
                self.setup_frame.start_inspection_button.after(reference_image_delay_milliseconds, lambda: self.take_reference_image())    #after x seconds take reference image
            
            else:
                self.take_reference_image()         #if a delay is not properly inputted, it will default to no delay


    def take_reference_image(self): #takes reference image by calling capture_reference_image from video_frame and enables fringe pattern button
        self.video_frame.capture_reference_image()
        self.controls_frame.fringe_pattern_button["state"] = "enabled"
        self.save_ref_image()   #once reference image is taken, save the image


    def inspection_limit(self):
        if self.inspection_time_limit_flag:
            if self.inspection_time_limit > 0:  #checking that the time limit set is valid
                inspection_time_limit_milliseconds = int(self.inspection_time_limit*1000*60)
                self.setup_frame.start_inspection_button.after(inspection_time_limit_milliseconds, lambda: self.inspection_limit_set())    #after x seconds take reference image


    def inspection_limit_set(self):
        self.pause()
        self.stop()
        print("limit reached")
    

    ######################## METHODS FOR INSPECTION SETUP ########################
    def inspection_time_limit_command(self):    #Sets flags to true or false and enables/disables buttons & entry based on checkbuttons status                   
        if self.setup_frame.inspection_time_limit_option.get():
            self.setup_frame.inspection_time_limit_entry["state"] = "enabled"                                      
            self.setup_frame.inspection_time_limit_set_button["state"] = "enabled"

            self.inspection_time_limit_flag = True                                          #inspection time limit flag (used in start method later)
        elif self.setup_frame.inspection_time_limit_option.get()==False:
            self.setup_frame.inspection_time_limit_entry["state"] = "disabled"
            self.setup_frame.inspection_time_limit_set_button["state"] = "disabled"

            self.inspection_time_limit_flag = False  
        

    def frame_capture_interval_command(self):   #Sets flags to true or false and enables/disables buttons & entry based on checkbuttons status            
        if self.setup_frame.frame_capture_interval_option.get():
            self.setup_frame.frame_capture_interval_entry["state"] = "enabled"
            self.setup_frame.frame_capture_interval_set_button["state"] = "enabled"

            self.frame_capture_interval_flag = True                                         #inspection time limit flag (used in start method later)
        elif self.setup_frame.frame_capture_interval_option.get()==False:
            self.setup_frame.frame_capture_interval_entry["state"] = "disabled"
            self.setup_frame.frame_capture_interval_set_button["state"] = "disabled"

            self.frame_capture_interval_flag = False 


    def reference_image_delay_command(self):    #Sets flags to true or false and enables/disables buttons & entry based on checkbuttons status             
        if self.setup_frame.reference_image_delay_option.get():
            self.setup_frame.reference_image_delay_entry["state"] = "enabled"
            self.setup_frame.reference_image_delay_set_button["state"] = "enabled"

            self.reference_image_delay_flag = True
        elif self.setup_frame.reference_image_delay_option.get()==False:
            self.setup_frame.reference_image_delay_entry["state"] = "disabled"
            self.setup_frame.reference_image_delay_set_button["state"] = "disabled"

            self.reference_image_delay_flag = True

    
    def inspection_time_limit_set(self):    #sets the inspection time limit time when set button is pressed
        try:
            self.inspection_time_limit = self.setup_frame.inspection_time_limit_mins.get()
            
            print(self.inspection_time_limit)
        except:
            print("error")
            self.inspection_time_limit = 0

    
    def frame_capture_interval_set(self):   #sets the frame capture interval time when set button is pressed
        try:
            self.frame_capture_interval = self.setup_frame.frame_capture_interval_seconds.get()
            
            print(self.frame_capture_interval)
        except:
            print("error")
            self.frame_capture_interval = 0

    
    def reference_image_delay_set(self):    #sets the reference image delay time when set button is pressed
        try:
            self.reference_image_delay = self.setup_frame.reference_image_delay_seconds.get()
            
            print(self.reference_image_delay)
        except:
            print("error")
            self.reference_image_delay = 0   #if this remains 0, there will be no reference image delay
    

    ######################## METHODS FOR CAMERA VARIABLES ########################