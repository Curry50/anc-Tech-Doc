// Auto-generated. Do not edit!

// (in-package franka_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class info {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.num = null;
      this.receive = null;
    }
    else {
      if (initObj.hasOwnProperty('num')) {
        this.num = initObj.num
      }
      else {
        this.num = 0.0;
      }
      if (initObj.hasOwnProperty('receive')) {
        this.receive = initObj.receive
      }
      else {
        this.receive = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type info
    // Serialize message field [num]
    bufferOffset = _serializer.float32(obj.num, buffer, bufferOffset);
    // Serialize message field [receive]
    bufferOffset = _arraySerializer.float32(obj.receive, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type info
    let len;
    let data = new info(null);
    // Deserialize message field [num]
    data.num = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [receive]
    data.receive = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.receive.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'franka_control/info';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '1c7aec7e51da1bf8a758e5a4abe8452d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 num
    float32[] receive
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new info(null);
    if (msg.num !== undefined) {
      resolved.num = msg.num;
    }
    else {
      resolved.num = 0.0
    }

    if (msg.receive !== undefined) {
      resolved.receive = msg.receive;
    }
    else {
      resolved.receive = []
    }

    return resolved;
    }
};

module.exports = info;
