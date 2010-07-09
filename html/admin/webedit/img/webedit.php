<?php
$tpl_webedit= new Smarty;
$tpl_webedit->compile_check = true;
$tpl_webedit->debugging = false;
$tpl_webedit->template_dir = $DOCUMENT_ROOT.'/smarty/templates/webedit/';
$tpl_webedit->compile_dir = $DOCUMENT_ROOT.'/smarty/templates_c/';
$tpl_webedit->config_dir = $DOCUMENT_ROOT.'/smarty/configs/';
$tpl_webedit->plugins_dir = $DOCUMENT_ROOT.'/smarty/plugins/';
$tpl_webedit->cache_dir = $DOCUMENT_ROOT.'/smarty/cache/';
$tpl_webedit->assign("WEBEDIT_JS",$WEBEDIT_JS);
$tpl_webedit->assign("WEBEDIT_PAGE",$WEBEDIT_PAGE);
foreach($WIZ as $key=>$val){
   $tpl_webedit->assign($key,$val);
}
$tpl_webedit->assign("value",$SITE_CONTENT);
ob_start();
$tpl_webedit->display('webedit.tpl');
$buffer_include=ob_get_contents();
ob_end_clean();


?>