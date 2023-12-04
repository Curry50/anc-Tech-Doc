;; Auto-generated. Do not edit!


(when (boundp 'franka_control::info)
  (if (not (find-package "FRANKA_CONTROL"))
    (make-package "FRANKA_CONTROL"))
  (shadow 'info (find-package "FRANKA_CONTROL")))
(unless (find-package "FRANKA_CONTROL::INFO")
  (make-package "FRANKA_CONTROL::INFO"))

(in-package "ROS")
;;//! \htmlinclude info.msg.html


(defclass franka_control::info
  :super ros::object
  :slots (_num _receive ))

(defmethod franka_control::info
  (:init
   (&key
    ((:num __num) 0.0)
    ((:receive __receive) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _num (float __num))
   (setq _receive __receive)
   self)
  (:num
   (&optional __num)
   (if __num (setq _num __num)) _num)
  (:receive
   (&optional __receive)
   (if __receive (setq _receive __receive)) _receive)
  (:serialization-length
   ()
   (+
    ;; float32 _num
    4
    ;; float32[] _receive
    (* 4    (length _receive)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _num
       (sys::poke _num (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32[] _receive
     (write-long (length _receive) s)
     (dotimes (i (length _receive))
       (sys::poke (elt _receive i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _num
     (setq _num (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32[] _receive
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _receive (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _receive i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get franka_control::info :md5sum-) "1c7aec7e51da1bf8a758e5a4abe8452d")
(setf (get franka_control::info :datatype-) "franka_control/info")
(setf (get franka_control::info :definition-)
      "float32 num
float32[] receive

")



(provide :franka_control/info "1c7aec7e51da1bf8a758e5a4abe8452d")


