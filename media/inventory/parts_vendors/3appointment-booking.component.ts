import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { add, addDays, addWeeks, startOfMonth, startOfWeek, sub, subWeeks } from 'date-fns';
import { DatePipe, Time } from "@angular/common";
import { FormsModule, FormControl, FormControlName, FormBuilder, FormGroup, Validators } from "@angular/forms";
import { TimeslotService } from 'src/app/services/timeslot/timeslot.service';
import { ToastrService } from "ngx-toastr";
import { NavigationExtras, Router } from "@angular/router";
import { CounsellorService } from 'src/app/services/counsellor/counsellor.service';
import { TimeslotBookingService } from 'src/app/services/timeslot-booking/timeslot-booking.service';
import {
  CalendarEvent,
  CalendarEventAction,
  CalendarEventTimesChangedEvent,
  CalendarView,
} from 'angular-calendar';
import { ActivatedRoute } from '@angular/router';
import { id } from 'date-fns/locale';
import { AppointmentBookingService } from 'src/app/services/appointment-booking/appointment-booking.service';
import * as moment from 'moment';
import { MatDialog } from '@angular/material/dialog';
import { DeleteDialogComponent } from 'src/app/theme/components/delete-dialog/delete-dialog.component';
import isThisHour from 'date-fns/esm/isThisHour/index';
import { UserCouponService } from 'src/app/services/user-coupon/user-coupon.service';
interface Day {
  date: Date;
  dayName: string;
}

interface TimeSlot {
  startTime: Date;
  endTime: Date;
}

interface Event {
  start: string;
  end: string;
}

@Component({
  selector: 'app-appointment-booking',
  templateUrl: './appointment-booking.component.html',
  styleUrls: ['./appointment-booking.component.sass'],
  providers: [DatePipe]
})

export class AppointmentBookingComponent {
  formgroup: FormGroup = new FormGroup({})
  currentDate: Date = new Date();
  currentDay = this.currentDate.getDay();
  startDate = new Date(this.currentDate);
  daysInWeek: { date: Date, dayName: string }[] = [];
  timeSlots: TimeSlot[] = [];
  slots: { date: any, start: any, end: any }[] = [];
  startTime: any
  endTime: any
  value!: number
  question!: string
  showSecondModal: boolean = false;
  selectedDuration: any;

  price: any
  // counsellor:any
  // counsellorData:any[] =[]
  // selectedTimeslotIndex:number=-1;
  selectedTimeslot: any
  openModal: boolean = false;
  view = CalendarView.Month;
  CalendarView = CalendarView
  endTimeArray: any[] = ['10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00'];
  // for modal
  selectedDay: any;
  confirmData!: FormGroup
  selectedStartTime: any
  bookingRadio!: FormGroup;

  //counsellor added timeslots
  counsellor_timeslot_event: { title: any, date: any, start: any, end: any }[] = []
  reservedStartTime: any
  reservedEndTime: any
  selectedPrice: any;
  //new array for time slot with this format HH:mm
  new_timeslot: any[] = []

  //endtime dropdown
  eTime: any
  selectedEndTime: any[] = []
  counsellorId: any;
  lang: any;

  //modes of counselling
  // mode_counselling: any 
  mode_counselling: any


  // for user booking
  confirmDate: any
  confirm_starttime: any
  confirm_endtime: any
  confirm_price_min: any
  isClicked = false;
  appointmentData: { date: any, start: any, end: any, status: any }[] = []
  response: any
  order_no: any
  therapist_languages: any;
  AskQuestion: boolean = false
  fomrdata: FormData;
  selectedMode: any;
  slotMode: any;
  slotorder_no: any;
  responseLink:any
  payment_status:any
  constructor(
    private datepipe: DatePipe,
    private formbuilder: FormBuilder,
    private timeslotService: TimeslotService,
    private toastrService: ToastrService,
    private cdr: ChangeDetectorRef,
    private getData: CounsellorService,
    private appointmentService: AppointmentBookingService,
    private bookingService: TimeslotBookingService,
    private activatedRouter: ActivatedRoute,
    private router: Router,
    private getUserCouponService: UserCouponService,
    private dialog: MatDialog
  ) {
    this.fomrdata = new FormData();
  }

  generateCalendar(): void {
    const today = new Date();
    const monday = startOfWeek(this.currentDate, { weekStartsOn: 1 });
    for (let i = 0; i < 7; i++) {
      const date = addDays(monday, i);
      const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
      this.daysInWeek.push({ dayName, date });
    }
    this.timeSlots = [];
    this.startTime = new Date();
    this.startTime.setHours(10, 0, 0, 0);
    // this.startTime = this.datepipe.transform(this.startTime,'HH:mm')

    this.endTime = new Date();
    this.endTime.setHours(19, 30, 0, 0);
    while (this.startTime.getTime() < this.endTime.getTime()) {
      this.timeSlots.push({
        startTime: new Date(this.startTime),
        endTime: new Date(this.startTime.getTime() + 30 * 60 * 1000),
      });
      this.startTime.setTime(this.startTime.getTime() + 30 * 60 * 1000);

    }
  }

  ngOnInit(): void {
    this.generateCalendar()
    this.submitSlot_booking()
    this.getTimeslots()
    this.getTimeslotBooking()
    this.getcounsellorData()
    this.getappointment_booking()
    this.getuserCoupono()

    this.mode_counselling = 'Video';
    // this.var = this.userCoupon.filter((mode: any) => mode.type === 'Video');
    this.selectedDuration = this.selectedPrice

    // console.log(this.mode_counselling);


    for (let i = 0; i < this.timeSlots.length; i++) {
      this.new_timeslot.push({
        startTime: this.datepipe.transform(this.timeSlots[i].startTime, 'HH:mm'),
        endTime: this.datepipe.transform(this.timeSlots[i].endTime, 'HH:mm'),
        startshowTime: this.timeSlots[i].startTime
      })
    }

    if (this.selectedPrice !== '15' && this.selectedPrice !== '30' && this.selectedPrice !== '60') {
      this.router.navigate(['/pages/get-matched/therapist-card'])
    }

  }
  //filterCouponByMode

  filterCouponByMode(){
    if (this.mode_counselling === 'Video') {
      this.var = this.userCoupon.filter((mode: any) => mode.type === 'Video');
    } else if (this.mode_counselling === 'Phone') {
      this.var = this.userCoupon.filter((mode: any) => mode.type === 'Phone');

    } else if (this.mode_counselling === 'Chat') {
      this.var = this.userCoupon.filter((mode: any) => mode.type === 'Chat');
    }
  }

  //mode sselection
  var: any
  mode_select(mode: any) {
    this.mode_counselling = mode
    // console.log(this.mode_counselling);
    this.filterCouponByMode();
  }

  start_time: any
  end_time: any
  formatDate: any

  //get booked slots
  getappointment_booking() {
    this.appointmentService.appointment_booking(this.counsellorId).subscribe((result: any) => {
      this.appointmentData = result
      // console.log(this.appointmentData);
      // console.log(this.counsellorId);
    })
  }

  userCoupon: any
  couponcode: any
  couponDis: any
  isCoupon: boolean = true;
  getuserCoupono() {
    this.getUserCouponService.getUserCoupons().subscribe((result) => {
      this.userCoupon = result;
      console.log(this.userCoupon);
      // this.couponid = this.userCoupon[0].coupon_id

      if(this.userCoupon === null){
        this.isCoupon = false;
        // console.log(this.isCoupon);
      }

      this.filterCouponByMode();
    })
  }

  // filterCoupon() {
  //   this.userCoupon.filter((mode: any) => mode.type === this.mode_counselling);
  //   console.log(this.filterCoupon());
  // }

  //actiating the coupon and change the color
  couponId: any = null
  clickCount: number = 0;
  amt: any
  unit: any
  savedPrice: any
  totalPrice: any
  couponCode: any
  couponDisAmt: any
  couponDisUnit: any
  showRemCoup: boolean = false
  coupon: any

  activateCoupon(value: any) {
    this.amt = value.discount_amt;
    this.unit = value.discount_unit;
    this.couponId = value.coupon_id;
    this.couponCode = value.coupon_code;

    //formdata to check the coupon is valid or not
    const couponData = new FormData();
    couponData.append('coupon_code', this.couponCode);

    this.getUserCouponService.checkUserCoupons(couponData).subscribe((result) => {

      this.couponDisAmt = result.discount_amt
      this.couponDisUnit = result.discount_unit

      if (this.couponDisUnit === '%') {
        this.savedPrice = (this.price * this.couponDisAmt) / 100;
        this.totalPrice = this.price - this.savedPrice;

        // console.log(this.totalPrice);
      } else {
        this.totalPrice = this.price - this.couponDisAmt
        this.savedPrice = this.couponDisAmt

        // console.log(this.totalPrice);
        // console.log(this.savedPrice);
      }

    })

    this.showRemCoup = !this.showRemCoup
  }

  removeCoupon() {
    this.couponId = null;
    this.couponDisUnit = null;
    if (this.couponDisUnit === null) {
      this.totalPrice = this.price
    }
  }



  //color change timeslot
  selectedTimeSlot(day: any, timeSlot: TimeSlot): void {
    this.formatDate = this.datepipe.transform(day.date, 'yyyy-MM-dd')
    const startFormat = new Date(`${this.formatDate}T${timeSlot.startTime}`)
    this.start_time = this.datepipe.transform(startFormat, 'hh:mm a')
    const endFormat = new Date(`${this.formatDate}T${timeSlot.endTime}`)
    this.end_time = this.datepipe.transform(endFormat, 'hh:mm a')

    if (this.selectedPrice === '15') {

      // this.start_time = timeSlot.startTime;
      // this.end_time = timeSlot.endTime;
      // console.log(this.start_time);
      // console.log(this.end_time);

      this.price = this.info?.price_15min
      this.confirm_price_min = '15'
      // console.log(this.price);
      this.lang = this.info?.language

    } else if (this.selectedPrice === '30') {
      // this.start_time = timeSlot.startTime;
      // this.end_time = timeSlot.endTime;
      this.price = this.info?.price_30min
      this.confirm_price_min = '30'
      this.lang = this.info?.language

    } else if (this.selectedPrice === '60') {
      for (let i = 0; i < this.appointmentData.length; i++) {

        if (this.formatDate === this.appointmentData[i].date && timeSlot.endTime === this.appointmentData[i].start && this.appointmentData[i].status === 'SUCCESS') {

          const warningModal = document.getElementById('warning-modal')
          const modal = document.getElementById('modal')
          if (warningModal != null) {
            warningModal.style.display = 'block'
            if (modal != null) {
              modal.style.display = 'none'
            }
          }
        } else {
          const e = new Date(endFormat.getTime() + 30 * 60 * 1000)
          this.end_time = this.datepipe.transform(e, 'hh:mm a')
          this.price = this.info?.price_60min
          this.confirm_price_min = '60'
          this.lang = this.info?.language
        }
      }


    }
    else {
      // this.router.navigate(['/pages/get-matched/therapist-card'])
    }
  }

  //schedule form
  submitSlot_booking() {
    this.formgroup = this.formbuilder.group({
      timeslot_date: new FormControl(''),
      starttime: new FormControl(''),
      endtime: new FormControl(''),
      price_min: new FormControl(''),
      user_description: new FormControl(null),
      mode: new FormControl('', Validators.required)
    })
  }

  get title() {
    return this.formgroup.get('title')
  }
  get endtime() {
    return this.formgroup.get('endtime');
  }
  get mode() {
    return this.formgroup.get('mode')
  }

  //today date
  istodaydate(date: Date) {
    const today = new Date();
    return date.getFullYear() === today.getFullYear() &&
      date.getMonth() === today.getMonth() &&
      date.getDate() === today.getDate();
  }

  settoday() {
    this.daysInWeek = []
    this.timeSlots = []
    this.currentDate = new Date()

    this.generateCalendar();

  }

  st_format: any
  isDisabled(date: any, stime: any, etime: any): boolean {


    const currentDate = new Date();
    const currentTime = currentDate.getTime();
    // console.log(st);
    const d = this.datepipe.transform(date, 'yyyy-MM-dd')
    const st = new Date(`${d}T${stime}:00`)
    const et = new Date(`${d}T${etime}:00`)
    this.reservedStartTime = this.datepipe.transform(st, 'HH:mm')
    this.reservedEndTime = this.datepipe.transform(et, 'HH:mm')

    for (let i = 0; i < this.counsellor_timeslot_event?.length; i++) {
      const starttime = this.counsellor_timeslot_event[i]['start']

      if (this.counsellor_timeslot_event[i].date === d) {
        // console.log(this.reservedStartTime);
        // console.log(this.counsellor_timeslot_event[i].start);

        if (this.counsellor_timeslot_event[i].start <= this.reservedStartTime && this.counsellor_timeslot_event[i].end > this.reservedStartTime ||
          this.counsellor_timeslot_event[i].start < this.reservedEndTime && this.counsellor_timeslot_event[i].end >= this.reservedEndTime) {
          return true;
        }
        // if (providedDateTime <  currentTime)
      }

    }
    const providedDateTime = new Date(date.getFullYear(), date.getMonth(), date.getDate(), st.getHours(), st.getMinutes()).getTime();
    // const modal = document.getElementById('modal');
    return providedDateTime < currentTime;
    // return true;
  }

  // get timeslots
  getTimeslots() {
    this.timeslotService.getTimeslot().subscribe((timeslots: any) => {

      this.counsellor_timeslot_event = timeslots
      // console.log(this.counsellor_timeslot_event);
    })
  }

  getTimeslotBooking() {
    this.counsellorId = this.activatedRouter.snapshot.params['id']
    this.selectedPrice = this.activatedRouter.snapshot.params['selectedprice']
    // console.log(this.selectedPrice);
    this.bookingService.booking_url(this.counsellorId).subscribe((data) => {
      this.counsellor_timeslot_event = data
      // console.log(this.counsellor_timeslot_event);
    })
  }

  st: any
  et: any
  // //set color if counsellor select otherwise not
  isBooked(date: any, stime: any, etime: any): boolean {
    const d = this.datepipe.transform(date, 'yyyy-MM-dd')


    const s = new Date(`${d}T${stime}:00`)
    const e = new Date(`${d}T${etime}:00`)
    this.reservedStartTime = this.datepipe.transform(s, 'HH:mm')
    this.reservedEndTime = this.datepipe.transform(e, 'HH:mm')
    // console.log(this.reservedEndTime,this.reservedStartTime);

    for (let i = 0; i < this.appointmentData?.length; i++) {
      const starttime = this.appointmentData[i]['start']
      // console.log(this.appointmentData[i].date === d);

      if (this.appointmentData[i].date === d) {
        // console.log(this.reservedStartTime);
        // console.log(this.counsellor_timeslot_event[i].start);

        if (this.appointmentData[i].start <= this.reservedStartTime && this.appointmentData[i].end > this.reservedStartTime ||
          this.appointmentData[i].start < this.reservedEndTime && this.appointmentData[i].end >= this.reservedEndTime) {
          if (this.appointmentData[i].status === 'SUCCESS') {

            return true
          }
        }
        // if (providedDateTime <  currentTime)
      }

    }
    return false
  }

  isInProcess(date: any, stime: any, etime: any): boolean {
    const d = this.datepipe.transform(date, 'yyyy-MM-dd')


    const s = new Date(`${d}T${stime}:00`)
    const e = new Date(`${d}T${etime}:00`)
    this.reservedStartTime = this.datepipe.transform(s, 'HH:mm')
    this.reservedEndTime = this.datepipe.transform(e, 'HH:mm')
    // console.log(this.reservedEndTime,this.reservedStartTime);

    for (let i = 0; i < this.appointmentData?.length; i++) {
      const starttime = this.appointmentData[i]['start']

      if (this.appointmentData[i].date === d) {
        // console.log(this.reservedStartTime);
        // console.log(this.counsellor_timeslot_event[i].start);

        if (this.appointmentData[i].start <= this.reservedStartTime && this.appointmentData[i].end > this.reservedStartTime ||
          this.appointmentData[i].start < this.reservedEndTime && this.appointmentData[i].end >= this.reservedEndTime) {
          if (this.appointmentData[i].status === 'INPROCESS') {

            return true
          }
        }
        // if (providedDateTime <  currentTime)
      }

    }
    return false
  }

  booked_slot: any
  // getBooking_slot(){
  //   this.booking_slot.booking_slot(this.counsellorId).subscribe((data)=>{
  //     this.booked_slot = data
  //     console.log(data);
  //   })
  // }

  info: any
  getcounsellorData() {
    this.getData.get_counsellor_id(this.counsellorId).subscribe((result) => {
      this.info = result;
      this.therapist_languages = this.info.language.split(',').join(', ')
      // console.log(this.info);
    })
  }

  getCurrentTime(): Date {
    return new Date();
  }

  onCalendarSelect(event: any) {

    this.timeSlots = [];
    this.daysInWeek = []
    this.currentDate = event;
    this.generateCalendar()

  }

  previousWeek(): void {
    this.currentDate = subWeeks(this.currentDate, 1);
    this.daysInWeek = []
    this.timeSlots = []
    this.generateCalendar();
  }

  nextWeek(): void {
    this.currentDate = addWeeks(this.currentDate, 1);
    this.daysInWeek = []
    this.timeSlots = []
    this.generateCalendar();
  }

  addEvent(day: { date: Date, dayName: string }, timeSlot: TimeSlot): void {
    // const startDate = new Date(day.date);
    // const startTime = new Date(timeSlot.startTime);
    // startDate.setHours(startTime.getHours(), startTime.getMinutes(), 0, 0);

    // const endDate = new Date(day.date);
    // const endTime = new Date(timeSlot.endTime);
    // endDate.setHours(endTime.getHours(), endTime.getMinutes(), 0, 0);

    // const event = {
    //   start:  this.datepipe.transform(startDate , 'dd-MM-yyyy hh:mm a'),
    //   end:   this.datepipe.transform(endDate , 'dd-MM-yyyy hh:mm a')
    // };
    // const index = this.counsellor_timeslot_event.findIndex((e:any) => e.start === event.start && e.end === event.end)

    // // const booked = this.isBooked(event.start,event.end)
    // // console.log(booked);

    // if(index !== -1){
    //   this.slots.splice(index, 1 );
    // }else{

    //   this.slots.push(event);

    // }
    // console.log(this.slots);

    //set endtime as selceted starttime
    this.selectedDay = day
    let sel_day = this.datepipe.transform(new Date(this.selectedDay.date), 'yyyy-MM-dd')
    this.selectedStartTime = new Date(`${sel_day}T${timeSlot.startTime}:00`)


    // let datetimestring = new Date(`${sel_day}T${this.selectedStartTime}:00`)

    // let startTime = this.datepipe.transform( datetimestring , 'HH:mm')   
    this.eTime = this.datepipe.transform(new Date(this.selectedStartTime.getTime()), 'hh:mm')
    // this.eTime = new Date(this.selectedStartTime.getTime() + 30 * 60 * 1000)
    // console.log(this.eTime);
    // console.log(this.endTimeArray);

    for (let i = 0; i < this.endTimeArray.length; i++) {
      if (this.eTime < this.endTimeArray[i]) {

        this.selectedEndTime.push(new Date(`${sel_day}T${this.endTimeArray[i]}:00`))
        // console.log(this.selectedEndTime);


      }
    }
    const modal = document.getElementById('modal');
    if (modal != null) {
      modal.style.display = 'block';
    }
  }



  resetVar(): boolean {
    if (this.selectedPrice === '30') {
      this.price = this.info?.price_30min
      // console.log(this.price);

      this.selectedDuration = this.selectedPrice
      // console.log(this.selectedDuration);

    }
    else if (this.selectedPrice === '15') {
      this.price = this.info?.price_15min
      // console.log(this.price);

      this.selectedDuration = this.selectedPrice
      // console.log(this.selectedDuration);

      // this.confirm_endtime = null;
    }
    else if (this.selectedPrice === '60') {
      this.price = this.info?.price_60min
      // console.log(this.price);

      this.selectedDuration = this.selectedPrice
      // console.log(this.selectedDuration);

    }
    // this.totalPrice = this.price
    return true;
  }

  //second modal close method
  secondmodal() {

    this.resetVar(); //reset all variables in changes by radio
    this.confirm_endtime = moment(this.confirm_endtime, 'hh:mm').format('hh:mm ')

    const confirmDialog = this.dialog.open(DeleteDialogComponent, {
      data: {
        title: 'Confirm TimeSlot Deletion',
        message: 'Are you sure, you want to delete this time slot?'
      }
    });

    confirmDialog.afterClosed().subscribe((result) => {
      if (result == true) {
        this.appointmentService.cancelSlot(this.order_no).subscribe((data: any) => {
          this.toastrService.warning('Your appointment is canceled!', 'Warning')
          this.getappointment_booking()
        })
        this.formgroup.reset()
        const modal = document.getElementById('modal');
        if (modal != null) {
          modal.style.display = 'none';
        }
        this.selectedEndTime = []

        const modelDiv = document.getElementById('second-modal');
        if (modelDiv != null) {
          modelDiv.style.display = 'none'
        }
      }


    })
    this.confirm_endtime = undefined

    return true;
  }
  slotdate: any

  //first modal close method
  firstClose() {
    const modal = document.getElementById('modal');
    if (modal != null) {
      modal.style.display = 'none';
    }
    this.resetVar();
    this.confirm_endtime = undefined

    this.removeCoupon();

  }

  //warning modal close
  warningModalClose() {
    const warningmodal = document.getElementById('warning-modal')
    if (warningmodal != null) {
      warningmodal.style.display = 'none'
    }

    // window.location.reload()
  }

  Modal30minutesClose() {
    const warningmodal = document.getElementById('warning-modal')
    if (warningmodal != null) {
      warningmodal.style.display = 'none'
    }
    this.selectedPrice = '30'
    // this.router.navigate([])
    // setTimeout(function(){
    //   window.location.reload()
    // },1000);
  }

  matdateSelect(event: any) {
    // console.log(event);
    this.timeSlots = []
    this.daysInWeek = []
    this.currentDate = event
    this.generateCalendar()
    this.view = CalendarView.Week
  }

  //for view month
  dayClicked({ date, events }: { date: Date; events: CalendarEvent[] }): void {
    // console.log('dayClicked', date, events);

    this.timeSlots = [];
    this.daysInWeek = []
    this.currentDate = date;
    this.generateCalendar()
    this.view = CalendarView.Week
  }

  activeDayIsOpen: boolean = true;
  closeOpenMonthViewDay() {
    this.activeDayIsOpen = false;
  }

  onConfirm() {
    // console.log(date,stime,etime);
    // this.slotdate = this.datepipe.transform(date, 'yyyy-MM-dd')
    // this.slots.push({ date: this.slotdate, start: stime, end: etime })
    // console.log(this.slots);
    console.log(this.response);

    // this.closemodal();
    if (this.response?.status === 'OK') {

      window.location.href = this.response.paymentLink
    }

  }

  selectedTimeRadio(duration: any) {
    this.selectedDuration = duration;

    if (this.selectedPrice === '15') {

      if (this.selectedDuration === '15') {
        this.price = this.info?.price_15min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;
        // console.log(this.end_time);


        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() - 15);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }

      if (this.selectedDuration === '30') {
        this.price = this.info?.price_30min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        // dateObj.setMinutes(dateObj.getMinutes() - 15);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }

      if (this.selectedDuration === '60') {
        this.price = this.info?.price_60min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() + 30);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }
    }
    if (this.selectedPrice === '30') {

      if (this.selectedDuration === '15') {
        this.price = this.info?.price_15min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;
        // console.log(this.price);

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() - 15);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }

      if (this.selectedDuration === '30') {
        this.price = this.info?.price_30min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;
        // console.log(this.price);

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        // dateObj.setMinutes(dateObj.getMinutes() - 30);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }

      if (this.selectedDuration === '60') {
        this.price = this.info?.price_60min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;
        // console.log(this.price);


        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() + 30);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }
    }
    if (this.selectedPrice === '60') {

      if (this.selectedDuration === '15') {
        this.price = this.info?.price_15min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() - 45);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);

      }

      if (this.selectedDuration === '30') {
        this.price = this.info?.price_30min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        dateObj.setMinutes(dateObj.getMinutes() - 30);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }

      if (this.selectedDuration === '60') {
        this.price = this.info?.price_60min;
        this.confirm_price_min = this.selectedDuration;
        this.confirm_endtime = this.end_time;

        const timeParts = this.confirm_endtime.split(':');
        const hours = parseInt(timeParts[0], 10);
        const minutes = parseInt(timeParts[1].split(' ')[0], 10);
        const meridian = timeParts[1].split(' ')[1];
        const dateObj = new Date();

        dateObj.setHours(hours);
        dateObj.setMinutes(minutes);
        dateObj.setSeconds(0);

        // dateObj.setMinutes(dateObj.getMinutes() - 30);

        let updatedHours = dateObj.getHours();
        let updatedMinutes = dateObj.getMinutes();
        let updatedMeridian = meridian;

        if (updatedHours === 0) {
          updatedHours = 12;
          updatedMeridian = 'PM';
        }

        const updatedTime = `${updatedHours}:${updatedMinutes < 10 ? '0' : ''}${updatedMinutes} ${updatedMeridian}`;

        this.confirm_endtime = updatedTime;

        // console.log(this.confirm_endtime);
      }
    }

  }

  getSlotDetails(){
    this.appointmentService.getOrder(this.slotorder_no).subscribe((order) => {
      // console.log(order);
      
    })
  }

  confirm_couponId: any
  responseData:any
  nextPayNow(date: any, stime: any, etime: any) {
    // console.log(this.confirm_endtime);
    this.confirmDate = this.datepipe.transform(date, 'yyyy-MM-dd')
    const s = moment(stime, 'hh:mm A').format('HH:mm')
    // console.log(s);
    const e = moment(etime, 'hh:mm A').format('HH:mm')
    // console.log(e);

    this.confirm_starttime = s

    if (this.confirm_endtime !== undefined) {
      this.confirm_endtime = moment(this.confirm_endtime, 'hh:mm A').format('HH:mm');
    } else {
      this.confirm_endtime = e
    }
    // console.log(this.confirm_starttime, this.confirm_endtime);

    const modelDiv = document.getElementById('second-modal');
    if (modelDiv != null) {
      modelDiv.style.display = 'block'
    }

    // this.confirmDate = date

    const formdata = new FormData()
    const formg = this.formgroup.value
    formdata.append('coupon_id', this.couponId)
    formdata.append('timeslot_date', this.confirmDate)
    formdata.append('starttime', this.confirm_starttime)
    formdata.append('endtime', this.confirm_endtime)
    formdata.append('price_min', this.confirm_price_min)
    formdata.append('mode', this.mode_counselling)
    if (formg.user_description) {

      formdata.append('user_description', formg.user_description.trim())
    } else {
      formdata.append('user_description', formg.user_description)

    }
 
    
    // console.log(formdata);
    this.appointmentService.submitSlot(this.counsellorId, formdata).subscribe((result: any) => {
      this.slotData = result
      // console.log(this.slotData);
      this.responseLink = result.response.paymentLink;
      this.payment_status = result.response.status
      // console.log(this.responseLink);
      
      this.slotorder_no = result.order_no
      // console.log(this.slotorder_no);
      this.getSlotDetails()
      this.getappointment_booking()
    }, (error: any) => {
      if (error?.error != undefined) {
        this.toastrService.warning(error?.error, 'Warning')
      }
      else {
        this.toastrService.warning('Internal server down! Please try after sometime', 'Warning')
      }

    
    })
    this.confirm_endtime = moment(this.confirm_endtime, 'hh:mm').format('hh:mm A');
    // this.confirm_endtime = this.end_time
  }
  confirmPayData !: any[] 
  slotData: any

  //ask any question method
  askQuestionMethod() {
    this.AskQuestion = !this.AskQuestion
  }

  //navigate through button
  gotoPayNow() {
    setTimeout(() => {
      const url = '/pages/' + this.counsellorId + '/appointment-booking-confirm/' + this.selectedPrice + '/' + this.slotorder_no;
      this.appointmentService.setPaymentLink(this.payment_status,this.responseLink)
      this.router.navigateByUrl(url);
    }, 5000);
  }
  

}
