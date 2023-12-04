; Auto-generated. Do not edit!


(cl:in-package franka_control-msg)


;//! \htmlinclude info.msg.html

(cl:defclass <info> (roslisp-msg-protocol:ros-message)
  ((num
    :reader num
    :initarg :num
    :type cl:float
    :initform 0.0)
   (receive
    :reader receive
    :initarg :receive
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass info (<info>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <info>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'info)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name franka_control-msg:<info> is deprecated: use franka_control-msg:info instead.")))

(cl:ensure-generic-function 'num-val :lambda-list '(m))
(cl:defmethod num-val ((m <info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader franka_control-msg:num-val is deprecated.  Use franka_control-msg:num instead.")
  (num m))

(cl:ensure-generic-function 'receive-val :lambda-list '(m))
(cl:defmethod receive-val ((m <info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader franka_control-msg:receive-val is deprecated.  Use franka_control-msg:receive instead.")
  (receive m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <info>) ostream)
  "Serializes a message object of type '<info>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'num))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'receive))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'receive))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <info>) istream)
  "Deserializes a message object of type '<info>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'num) (roslisp-utils:decode-single-float-bits bits)))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'receive) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'receive)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<info>)))
  "Returns string type for a message object of type '<info>"
  "franka_control/info")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'info)))
  "Returns string type for a message object of type 'info"
  "franka_control/info")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<info>)))
  "Returns md5sum for a message object of type '<info>"
  "1c7aec7e51da1bf8a758e5a4abe8452d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'info)))
  "Returns md5sum for a message object of type 'info"
  "1c7aec7e51da1bf8a758e5a4abe8452d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<info>)))
  "Returns full string definition for message of type '<info>"
  (cl:format cl:nil "float32 num~%float32[] receive~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'info)))
  "Returns full string definition for message of type 'info"
  (cl:format cl:nil "float32 num~%float32[] receive~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <info>))
  (cl:+ 0
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'receive) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <info>))
  "Converts a ROS message object to a list"
  (cl:list 'info
    (cl:cons ':num (num msg))
    (cl:cons ':receive (receive msg))
))
