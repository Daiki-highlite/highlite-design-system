// Monthly billing reminder for channel C07T3NBB18W
// Fires on the 22nd (main message) and 24th (final thread reply) of each month.
// Setup: run setupBillingReminderTrigger() once from the GAS editor.

var CHANNEL_ID = 'C07T3NBB18W';
var FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd-j1SlKcpjell6kJH2B-N9SWOBciGgIBG-GnRpN58Pjxu-8w/viewform?usp=dialog';

function getBillingReminderText_(year, month) {
  return '<!here>\n'
    + ':kotori:*請求書送付のご案内*　' + year + '年' + month + '月分:nushi:\n\n'
    + 'Highlite協力者、Lapidaristの皆さま、お疲れ様です！\n\n'
    + '委託対象者の皆さまへ、' + month + '月稼働分の請求書および経費申請についてのリマインドです\n'
    + 'Gフォームでの送付をお願いいたします:love:\n\n'
    + '以下フォームにて請求書をお送りください。\n'
    + '不明点あったらSlackで返信いただいて！\n'
    + 'お手数ですが、よろしくお願いします。\n\n'
    + ':engineko-tsurime:*【請求書送付フォームは→<' + FORM_URL + '|こちら>】*\n'
    + '*締切：' + month + '/27まで*';
}

function getFinalReminderText_(month) {
  return '<!here>\n'
    + ':engineko-tsurime: *【最終リマインド】締切は' + month + '/27です！*\n\n'
    + 'まだ請求書の送付がお済みでない方は、' + month + '/27（締切）までに\n'
    + 'Gフォームからの送付をお願いします:love:\n\n'
    + ':engineko-tsurime:*【請求書送付フォームは→<' + FORM_URL + '|こちら>】*\n'
    + '*締切：' + month + '/27まで*';
}

function checkAndSendBillingReminder() {
  var jst = new Date(new Date().getTime() + 9 * 60 * 60 * 1000);
  var day = jst.getUTCDate();
  var month = jst.getUTCMonth() + 1;
  var year = jst.getUTCFullYear();

  if (day === 22) {
    sendMainBillingReminder_(year, month);
  } else if (day === 24) {
    sendFinalBillingReminder_(year, month);
  }
}

function sendMainBillingReminder_(year, month) {
  var token = PropertiesService.getScriptProperties().getProperty('SLACK_BOT_TOKEN');
  if (!token) throw new Error('SLACK_BOT_TOKEN not set in Script Properties');
  var text = getBillingReminderText_(year, month);

  var options = {
    method: 'post',
    contentType: 'application/json; charset=utf-8',
    headers: { Authorization: 'Bearer ' + token },
    payload: JSON.stringify({ channel: CHANNEL_ID, text: text }),
    muteHttpExceptions: true
  };

  var data = JSON.parse(UrlFetchApp.fetch('https://slack.com/api/chat.postMessage', options).getContentText());
  if (data.ok) {
    PropertiesService.getScriptProperties()
      .setProperty('BILLING_REMINDER_TS_' + year + '_' + month, data.ts);
  } else {
    Logger.log('sendMainBillingReminder_ error: ' + data.error);
  }
}

function sendFinalBillingReminder_(year, month) {
  var token = PropertiesService.getScriptProperties().getProperty('SLACK_BOT_TOKEN');
  if (!token) throw new Error('SLACK_BOT_TOKEN not set in Script Properties');
  var threadTs = PropertiesService.getScriptProperties()
    .getProperty('BILLING_REMINDER_TS_' + year + '_' + month);
  if (!threadTs) throw new Error('Thread ts not found for ' + year + '/' + month);

  var options = {
    method: 'post',
    contentType: 'application/json; charset=utf-8',
    headers: { Authorization: 'Bearer ' + token },
    payload: JSON.stringify({ channel: CHANNEL_ID, text: getFinalReminderText_(month), thread_ts: threadTs }),
    muteHttpExceptions: true
  };

  var data = JSON.parse(UrlFetchApp.fetch('https://slack.com/api/chat.postMessage', options).getContentText());
  if (!data.ok) Logger.log('sendFinalBillingReminder_ error: ' + data.error);
}

function setupBillingReminderTrigger() {
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'checkAndSendBillingReminder') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('checkAndSendBillingReminder')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
  Logger.log('Billing reminder trigger installed (daily at 9:00 in script timezone).');
}
