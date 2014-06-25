<?php

set_include_path(get_include_path() . PATH_SEPARATOR . '../lib');

include_once("aur.inc.php");
include_once("pkgfuncs.inc.php");

set_lang();
check_sid();

html_header(__("Package Merging"));

$atype = "";

if (isset($_COOKIE["AURSID"])) {
	$atype = account_from_sid($_COOKIE["AURSID"]);
}

if ($atype == "Trusted User" || $atype == "Developer"): ?>
<div class="box">
	<h2><?= __('Merge Package: %s', htmlspecialchars($pkgbase_name)) ?></h2>
	<p>
		<?= __('Use this form to merge the package base %s%s%s into another package. ',
			'<strong>', htmlspecialchars($pkgbase_name), '</strong>'); ?>
		<?= __('The following packages will be deleted: '); ?>
	</p>
	<ul>
		<?php foreach(pkgbase_get_pkgnames($base_id) as $pkgname): ?>
		<li><?= htmlspecialchars($pkgname) ?></li>
		<?php endforeach; ?>
	</ul>
	<p>
		<?= __('Once the package has been merged it cannot be reversed. '); ?>
		<?= __('Enter the package name you wish to merge the package into. '); ?>
		<?= __('Select the checkbox to confirm action.') ?>
	</p>
	<form action="<?= get_uri('/pkgbase/'); ?>" method="post">
		<fieldset>
			<input type="hidden" name="IDs[<?= $base_id ?>]" value="1" />
			<input type="hidden" name="ID" value="<?= $base_id ?>" />
			<input type="hidden" name="token" value="<?= htmlspecialchars($_COOKIE['AURSID']) ?>" />
			<?php if (isset($_GET['via'])): ?>
			<input type="hidden" name="via" value="<?= intval($_GET['via']) ?>" />
			<?php endif; ?>
			<p><label for="merge_Into" ><?= __("Merge into:") ?></label>
			<input type="text" id="merge_Into" name="merge_Into" value="<?= isset($_GET['into']) ? $_GET['into'] : '' ?>" /></p>
			<p><input type="checkbox" name="confirm_Delete" value="1" />
			<?= __("Confirm package merge") ?></p>
			<p><input type="submit" class="button" name="do_Delete" value="<?= __("Merge") ?>" /></p>
		</fieldset>
	</form>
</div>

<?php else:
	print __("Only Trusted Users and Developers can merge packages.");
endif;

html_footer(AUR_VERSION);
