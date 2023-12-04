; Auto-generated. Do not edit!


(cl:in-package libfranka-msg)


;//! \htmlinclude info.msg.html

(cl:defclass <info> (roslisp-msg-protocol:ros-message)
  ((num
    :reader num
    :initarg :num
    :type cl:integer
    :initform 0))
)

(cl:defclass info (<info>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <info>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'info)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name libfranka-msg:<info> is deprecated: use libfranka-msg:info instead.")))

(cl:ensure-generic-function 'num-val :lambda-list '(m))
(cl:defmethod num-val ((m <info>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader libfranka-msg:num-val is deprecated.  Use libfranka-msg:num instead.")
  (num m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <info>) ostream)
  "Serializes a message object of type '<info>"
  (cl:let* ((signed (cl:slot-value msg 'num)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 18446744073709551616) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <info>) istream)
  "Deserializes a message object of type '<info>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'num) (cl:if (cl:< unsigned 9223372036854775808) unsigned (cl:- unsigned 18446744073709551616))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<info>)))
  "Returns string type for a message object of type '<info>"
  "libfranka/info")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'info)))
  "Returns string type for a message object of type 'info"
  "libfranka/info")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<info>)))
  "Returns md5sum for a message object of type '<info>"
  "57d3c40ec3ac3754af76a83e6e73127a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'info)))
  "Returns md5sum for a message object of type 'info"
  "57d3c40ec3ac3754af76a83e6e73127a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<info>)))
  "Returns full string definition for message of type '<info>"
  (cl:format cl:nil "int64 num~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'info)))
  "Returns full string definition for message of type 'info"
  (cl:format cl:nil "int64 num~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <info>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <info>))
  "Converts a ROS message object to a list"
  (cl:list 'info
    (cl:cons ':num (num msg))
))
