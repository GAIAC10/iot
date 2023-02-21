
    function Add_li() {　
        // target表示的是模板文件中的对象
　　　　var addli_html = Template('test-item',{'target':data});　　
        // 在ul后面append
       $("test-artTemplate").append(addli_html)
    }
