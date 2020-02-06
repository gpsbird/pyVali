===========
pyVali
===========

**pyVali** is a validation tool for python

.. code-block:: python

    from pyVali import Int, Float, Str, Dict, List

    value = {
        "user_id": "32495732",
        "score": 3.5,
        "telephone": "13234566543",
        "user_type": 2,
        "question_list": [{
            "question_id": "asdfsdf",
            "question": "你好？",
            "answer": "我很好，你是谁？",
            "status": 0,
        }]
    }
    schema = Dict({
        "user_id": Int(comment="用户id", ),
        "score": Float(comment="用户评分", min_value=0, max_value=5),
        "telephone": Str(comment="用户电话号码", min_length=11, max_length=11, pattern=r"^1[3456789]\d{9}$"),
        "user_type": Int(comment="用户类型", enum=[0, 1, 2, 3]),
        "question_list": List(
            struct=[Dict(
                {"question_id": Str(comment="问题id"),
                 "question": Str(comment="问题"),
                 "answer": Str(comment="回答"),
                 "status": Int(comment="状态")},
                comment="问题")],
            comment="问题列表", )
    })
    errMsg, value = schema.validate(value)
    if errMsg:
        raise Exception(errMsg)
    print(errMsg, value)

