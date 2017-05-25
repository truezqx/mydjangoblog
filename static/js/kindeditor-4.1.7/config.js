KindEditor.ready(function(K) {
    K.create('textarea[name=content]',{

        // 指定大小
        width:'1000px',
        height:'500px',
        uploadJson:'/admin/upload/kindeditor',
    });
});