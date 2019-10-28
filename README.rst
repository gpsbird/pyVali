===========
pyVali
===========

**pyVali** is a validation tool for python

.. code-block:: python

    from pyVali import Int,Float,Str,Dict,List

    value = {
        "user_id": 123,
        "tenant_id": 345,
        "question_list": [{
            "question_id": "asdfsdf",
            "question": "你好？",
            "answer": "我很好，你是谁？",
            "status": 0,
        }]
    }
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[Dict(
                {"question_id": Str(comment="问题id"),
                 "question": Str(comment="问题"),
                 "answer": Str(comment="回答"),
                 "status": Int(comment="状态")},
                comment="问题")],
            comment="问题列表")
    })

    print(schema.validate(value))

    sub_schema = Dict(struct={"question_id": Str(comment="问题id"),
                              "question": Str(comment="问题"),
                              "answer": Str(comment="回答"),
                              "status": Int(comment="状态")},
                      comment="问题")
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[sub_schema, ],
            comment="问题列表")
    })
    err, value = schema.validate(value)

